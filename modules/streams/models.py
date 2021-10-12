from datetime import datetime
from modules.shared.models import BaseModel, peewee


class Stream(BaseModel):
    name = peewee.CharField(max_length=255, unique=True)
    time_paused = peewee.TimeField()

    def __str__(self):
        return self.name


def create_tables():
    tables = [
        ('Stream', Stream),
    ]
    for table in tables:
        print(f'Creating table {table[0]}')
        table[1].create_table()
