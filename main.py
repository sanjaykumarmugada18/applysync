from contextlib import asynccontextmanager
from threading import Lock
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from applications import router
from config import ConfigurationError
from auth import router as auth_router, AttemptLimiter
from auth_config import allowed_origins
from fastapi.exceptions import RequestValidationError
from gmail_routes import router as gmail_router


class OAuthAccessFilter(logging.Filter):
    def filter(self, record):
        # Uvicorn's default access line contains query strings, including codes.
        return "/gmail/callback" not in record.getMessage()


logging.getLogger("uvicorn.access").addFilter(OAuthAccessFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        if app.state.engine is not None:
            app.state.engine.dispose()
            app.state.engine = None


async def database_error(request: Request, error: Exception):
    # Do not log or serialize the exception, SQL, parameters, or configuration.
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def health():
    return {"status": "healthy"}


def create_app(database_target: str = "dev") -> FastAPI:
    if database_target not in {"dev", "test"}:
        raise ConfigurationError("Database target must be dev or test.")
    application = FastAPI(lifespan=lifespan)
    origins = allowed_origins()

    @application.middleware("http")
    async def request_security(request: Request, call_next):
        # Independent server checks: simple forms, absent/foreign origins, and
        # missing custom headers are rejected even without a CORS preflight.
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            if (request.headers.get("origin") not in origins
                    or request.headers.get("x-applysync-csrf") != "1"):
                return JSONResponse(status_code=403, content={"detail": "Request protection failed"})
        response = await call_next(request)
        if request.url.path.startswith(("/auth", "/applications", "/gmail")):
            response.headers["Cache-Control"] = "no-store"
        if request.url.path == "/gmail/callback":
            response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @application.exception_handler(RequestValidationError)
    async def safe_validation(request, error):
        # FastAPI's default input echo can include submitted passwords.
        return JSONResponse(status_code=422, content={"detail": [
            {"loc": list(item["loc"]), "type": item["type"], "msg": "Invalid input"}
            for item in error.errors()]})
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(origins),
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-ApplySync-CSRF"],
    )
    application.state.database_target = database_target
    application.state.engine = None
    application.state.engine_lock = Lock()
    application.state.attempt_limiter = AttemptLimiter()
    application.add_exception_handler(SQLAlchemyError, database_error)
    application.add_exception_handler(ConfigurationError, database_error)
    application.add_api_route("/health", health, methods=["GET"])
    application.include_router(router)
    application.include_router(auth_router)
    application.include_router(gmail_router)
    return application


app = create_app()
