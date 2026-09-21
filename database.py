"""Engine creation and explicit commit/rollback boundaries."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from config import DatabaseSettings


def build_engine(settings: DatabaseSettings) -> Engine:
    return create_engine(settings.url(), pool_pre_ping=True, echo=False,
                         hide_parameters=True, connect_args={"connect_timeout": 5})


@contextmanager
def session_scope(engine: Engine):
    # begin() commits on success and rolls back on exceptions; close always runs.
    with Session(engine) as session:
        with session.begin():
            yield session
