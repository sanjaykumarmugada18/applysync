from unittest.mock import MagicMock

import pytest

from scripts import setup_databases


@pytest.mark.parametrize("existing", ["database", "role"])
def test_existing_names_stop_before_writes(existing, monkeypatch, tmp_path):
    monkeypatch.setattr(setup_databases, "ROOT", tmp_path)
    connection = MagicMock()
    cursor = connection.execute.return_value
    cursor.fetchone.side_effect = [(1,)] if existing == "database" else [None, (1,)]
    with pytest.raises(RuntimeError):
        setup_databases.provision(connection, {})
    assert not (tmp_path / ".env").exists()
    assert all(call.args[0].startswith("SELECT") for call in connection.execute.call_args_list)


def test_existing_configuration_is_never_overwritten(monkeypatch, tmp_path):
    monkeypatch.setattr(setup_databases, "ROOT", tmp_path)
    connection = MagicMock()
    connection.execute.return_value.fetchone.return_value = None
    path = tmp_path / ".env"
    path.write_text("synthetic-existing-content")
    with pytest.raises(FileExistsError):
        setup_databases.provision(connection, {name: "synthetic" for name in setup_databases.NAMES})
    assert path.read_text() == "synthetic-existing-content"
    assert all(call.args[0].startswith("SELECT") for call in connection.execute.call_args_list)
