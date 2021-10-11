from datetime import datetime

import peewee

from modules.shared.models import BaseModel, schemas, peewee


class Stream(BaseModel):
    name = peewee.CharField(max_length=255, unique=True)
    time_paused = peewee.DateField()

    def __str__(self):
        return self.name


def create_tables():
    tables = [
        ('Stream', Stream),
    ]
    for table in tables:
        table[1].create_table()
