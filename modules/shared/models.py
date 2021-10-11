import peewee

database_name = 'series_and_movies_db'

pg_db = peewee.PostgresqlDatabase(database_name, user='postgres', password='1234',
                                  host='127.0.0.1', port=5435)

schemas = {
    'streams': 'streams',
}


class BaseModel(peewee.Model):
    class Meta:
        database = pg_db
