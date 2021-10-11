import os
import psycopg2
import peewee
from playhouse.db_url import connect


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# database_name = 'series_and_movies_db'

# pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='1234',
#                                   host='127.0.0.1', port=5435)

pg_db = connect(DATABASE_URL)
print(f'[*] DATABASE CONNECTED TO {DATABASE_URL}')


class BaseModel(peewee.Model):
    class Meta:
        database = pg_db
