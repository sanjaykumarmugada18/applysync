"""Migrate only the explicitly selected dedicated local database."""

from alembic import context
from alembic.util import CommandError
from sqlalchemy.exc import SQLAlchemyError

from config import ConfigurationError, load_settings
from database import build_engine
from models import Base

target_metadata = Base.metadata


def run_migrations():
    target = context.get_x_argument(as_dictionary=True).get("target", "dev")
    try:
        settings = load_settings(target)
        if context.is_offline_mode():
            context.configure(dialect_name="postgresql", target_metadata=target_metadata,
                              literal_binds=True)
            with context.begin_transaction():
                context.run_migrations()
        else:
            engine = build_engine(settings)
            try:
                with engine.connect() as connection:
                    context.configure(connection=connection, target_metadata=target_metadata,
                                      compare_type=True)
                    with context.begin_transaction():
                        context.run_migrations()
            finally:
                engine.dispose()
    except ConfigurationError as error:
        raise CommandError(str(error)) from None
    except SQLAlchemyError:
        raise CommandError("Database migration failed; check local access and schema. Details suppressed.") from None


run_migrations()
