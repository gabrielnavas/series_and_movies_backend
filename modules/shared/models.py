import os
import psycopg2
import peewee
from playhouse.db_url import connect


def get_heroku_db_connection():
    HEROKU_DATABASE_URL = os.environ['DATABASE_URL']
    pg_db = connect(HEROKU_DATABASE_URL)
    return pg_db


def get_dev_local_db_connection():
    database_name = 'amazon_dev_db'
    pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='dev_password',
                                      host='127.0.0.1', port=5435)
    return pg_db


def make_db_connection():
    pg_db = None

    env_now = os.getenv['env']
    if env_now == 'dev':
        pg_db = get_heroku_db_connection()
    elif env_now == 'prod':
        pg_db = get_dev_local_db_connection()
    else:
        raise Exception('NEED SETTING env=dev or env=prod')
    return pg_db


class BaseModel(peewee.Model):
    class Meta:
        database = make_db_connection()
