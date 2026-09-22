"""Local manual create/list/detail endpoints and their database operations."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.engine import Engine

from database import get_engine, session_scope
from models import JobApplication
from schemas import ApplicationCreate, ApplicationPage, ApplicationRead

router = APIRouter(prefix="/applications", tags=["applications"])
DatabaseEngine = Annotated[Engine, Depends(get_engine)]


@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, engine: DatabaseEngine):
    with session_scope(engine) as session:
        application = JobApplication(**payload.model_dump())
        session.add(application)
        session.flush()
        # Materialize while attached; no lazy loads after commit/close.
        response = ApplicationRead.model_validate(application)
    # session_scope must commit successfully before the response can be returned.
    return response


@router.get("", response_model=ApplicationPage)
def list_applications(
    engine: DatabaseEngine,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0, le=10_000)] = 0,
):
    with session_scope(engine) as session:
        rows = session.scalars(select(JobApplication).order_by(
            JobApplication.created_at.asc(), JobApplication.id.asc()
        ).limit(limit).offset(offset))
        response = ApplicationPage(items=[ApplicationRead.model_validate(row) for row in rows],
                                   limit=limit, offset=offset)
    return response


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: UUID, engine: DatabaseEngine):
    with session_scope(engine) as session:
        application = session.get(JobApplication, application_id)
        if application is None:
            raise HTTPException(status_code=404, detail="Application not found")
        response = ApplicationRead.model_validate(application)
    return response
