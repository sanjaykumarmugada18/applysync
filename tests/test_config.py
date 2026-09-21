import pytest

from config import ConfigurationError, load_settings


def valid_env():
    return {"APPLYSYNC_DB_HOST": "127.0.0.1", "APPLYSYNC_DB_PORT": "5432",
            "APPLYSYNC_TEST_DB_NAME": "applysync_test", "APPLYSYNC_TEST_DB_USER": "applysync_test",
            "APPLYSYNC_TEST_DB_PASSWORD": "synthetic-password:@/%"}


def test_missing_configuration_is_safe():
    with pytest.raises(ConfigurationError, match="settings are missing"):
        load_settings("test", environ={}, env_file=None)


@pytest.mark.parametrize("key,value", [
    ("APPLYSYNC_DB_PORT", "synthetic-password"), ("APPLYSYNC_DB_PORT", "0"),
    ("APPLYSYNC_DB_HOST", "external.invalid"),
    ("APPLYSYNC_TEST_DB_NAME", "applysync_dev"),
    ("APPLYSYNC_TEST_DB_USER", "applysync_dev"),
    ("APPLYSYNC_TEST_DB_PASSWORD", "replace-with-local-test-password"),
])
def test_invalid_configuration_never_echoes_values(key, value):
    values = valid_env()
    values[key] = value
    with pytest.raises(ConfigurationError) as caught:
        load_settings("test", environ=values, env_file=None)
    assert value not in str(caught.value)
    assert values["APPLYSYNC_TEST_DB_PASSWORD"] not in str(caught.value)


def test_password_characters_and_repr():
    values = valid_env()
    settings = load_settings("test", environ=values, env_file=None)
    assert settings.url().password == values["APPLYSYNC_TEST_DB_PASSWORD"]
    assert values["APPLYSYNC_TEST_DB_PASSWORD"] not in repr(settings)


def test_environment_overrides_dotenv_without_interpolation(tmp_path):
    path = tmp_path / "example"
    path.write_text("APPLYSYNC_DB_PORT=1\nAPPLYSYNC_TEST_DB_PASSWORD='${LITERAL}'\n")
    values = valid_env()
    del values["APPLYSYNC_TEST_DB_PASSWORD"]
    settings = load_settings("test", environ=values, env_file=path)
    assert settings.port == 5432
    assert settings.password == "${LITERAL}"
