import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config import ConfigurationError, load_settings
from database import build_engine


def pytest_addoption(parser):
    parser.addoption("--run-db", action="store_true", help="Require the dedicated migrated test database")


@pytest.fixture
def test_engine(request):
    if not request.config.getoption("--run-db"):
        pytest.skip("Pass --run-db after provisioning and migrating the dedicated test database")
    engine = None
    try:
        engine = build_engine(load_settings("test"))
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT current_database()")) == "applysync_test"
            assert connection.scalar(text("SELECT current_user")) == "applysync_test"
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
        yield engine
    except (ConfigurationError, SQLAlchemyError):
        pytest.fail("Dedicated test database is not configured, reachable, or migrated.", pytrace=False)
    finally:
        if engine is not None:
            engine.dispose()
