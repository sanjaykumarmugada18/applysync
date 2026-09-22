"""Engine creation and explicit commit/rollback boundaries."""

from contextlib import contextmanager

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from config import DatabaseSettings, load_settings


def build_engine(settings: DatabaseSettings) -> Engine:
    return create_engine(settings.url(), pool_pre_ping=True, echo=False,
                         hide_parameters=True, connect_args={"connect_timeout": 5})


def get_engine(request: Request) -> Engine:
    """One lazily initialized engine per app; health needs no configuration."""
    state = request.app.state
    with state.engine_lock:
        if state.engine is None:
            state.engine = build_engine(load_settings(state.database_target))
        return state.engine


@contextmanager
def session_scope(engine: Engine):
    # begin() commits on success and rolls back on exceptions; close always runs.
    with Session(engine) as session:
        with session.begin():
            yield session
