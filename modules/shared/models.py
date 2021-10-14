import os
import psycopg2
import peewee
from playhouse.db_url import connect
from main.env import ENV_NOW, HEROKU_DATABASE_URL


def get_heroku_db_connection():
    pg_db = connect(HEROKU_DATABASE_URL)
    return pg_db


def get_dev_local_db_connection():
    database_name = 'series_movies_dev_db'
    pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='dev_password',
                                      host='127.0.0.1', port=5433)
    print(database_name)
    return pg_db


def get_test_local_db_connection():
    database_name = 'series_movies_test_db'
    pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='test_password',
                                      host='127.0.0.1', port=5435)
    return pg_db


def make_db_connection():
    pg_db = None
    connections = {
        'prod':  get_heroku_db_connection,
        'dev':  get_dev_local_db_connection,
        'test':  get_test_local_db_connection,
    }
    try:
        connection_db = connections[ENV_NOW]
        pg_db = connection_db()
    except Exception as ex:
        raise Exception('NEED SETTING env=dev; env=prod; env=test')

    return pg_db


class BaseModel(peewee.Model):
    class Meta:
        database = make_db_connection()
