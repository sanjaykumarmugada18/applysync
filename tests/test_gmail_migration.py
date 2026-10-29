"""Preservation rehearsal in a rolled-back schema, never development data."""
from uuid import uuid4
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text


def test_gmail_upgrade_preserves_existing_rows(test_engine):
    schema = 'migration_test_' + uuid4().hex
    with test_engine.connect() as connection:
        transaction = connection.begin()
        try:
            assert connection.scalar(text('select current_database()')) == 'applysync_test'
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
            config = Config('alembic.ini'); config.attributes['connection'] = connection
            command.upgrade(config, '0002')
            user, session_id, owned, legacy = [uuid4() for _ in range(4)]
            connection.execute(text("insert into users(id,email,password_hash) values (:id,'synthetic@example.com','synthetic-placeholder')"), {'id':user})
            connection.execute(text("insert into auth_sessions(id,user_id,expires_at) values (:id,:owner,now()+interval '1 hour')"), {'id':session_id,'owner':user})
            for id_, owner in [(owned,user),(legacy,None)]:
                connection.execute(text("insert into job_applications(id,company,role,applied_on,owner_id) values (:id,'Synthetic','Engineer',current_date,:owner)"), {'id':id_,'owner':owner})
            tables = ['users','auth_sessions','job_applications']
            before = {t: connection.execute(text(f'SELECT * FROM {t} ORDER BY id')).all() for t in tables}
            command.upgrade(config,'0003'); command.upgrade(config,'head')
            assert before == {t: connection.execute(text(f'SELECT * FROM {t} ORDER BY id')).all() for t in tables}
            assert connection.scalar(text('select version_num from alembic_version')) == '0003'
            assert set(inspect(connection).get_table_names(schema=schema)) == set(tables+['alembic_version','gmail_connections','gmail_oauth_states'])
            assert inspect(connection).get_pk_constraint('gmail_connections')['constrained_columns'] == ['owner_id']
            assert len(inspect(connection).get_foreign_keys('gmail_oauth_states')) == 2
        finally:
            transaction.rollback()
