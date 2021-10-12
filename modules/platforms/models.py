from modules.shared.models import BaseModel, peewee


class Platform(BaseModel):
    name = peewee.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def create_tables():
    tables = [
        ('Platform', Platform),
    ]
    for table in tables:
        print(f'Creating table {table[0]}')
        table[1].create_table()
