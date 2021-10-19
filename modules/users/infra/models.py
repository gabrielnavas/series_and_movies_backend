from datetime import datetime

from modules.shared.models import BaseModel, peewee


class User(BaseModel):

    first_name = peewee.CharField(max_length=180, null=False)
    last_name = peewee.CharField(max_length=100, null=False)
    email = peewee.CharField(max_length=180, unique=True)
    password = peewee.CharField(null=False)
    created_at = peewee.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def create_tables():
    tables = [
        ('User', User),
    ]
    for table in tables:
        print(f'Creating table {table[0]}')
        table[1].create_table()
