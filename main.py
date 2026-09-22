from contextlib import asynccontextmanager
from threading import Lock

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from applications import router
from config import ConfigurationError


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
    application.state.database_target = database_target
    application.state.engine = None
    application.state.engine_lock = Lock()
    application.add_exception_handler(SQLAlchemyError, database_error)
    application.add_exception_handler(ConfigurationError, database_error)
    application.add_api_route("/health", health, methods=["GET"])
    application.include_router(router)
    return application


app = create_app()
