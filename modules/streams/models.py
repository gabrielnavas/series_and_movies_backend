from modules.shared.models import BaseModel, peewee
from modules.platforms.models import Platform


class Stream(BaseModel):
    name = peewee.CharField(max_length=255, unique=True)
    time_paused = peewee.TimeField()
    platform = peewee.ForeignKeyField(Platform, on_delete='RESTRICT')

    def __str__(self):
        return self.name


def create_tables():
    tables = [
        ('Stream', Stream),
    ]
    for table in tables:
        print(f'Creating table {table[0]}')
        table[1].create_table()
