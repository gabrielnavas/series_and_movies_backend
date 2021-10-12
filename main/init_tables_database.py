from modules.streams.models import Stream


def init_tables():
    Stream.create_table()
