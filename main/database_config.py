from modules.streams.models import Stream
from modules.platforms.models import Platform


class DatabaseConfig:
    def handle(self):
        self.__create_tables()
        self.__add_initial_data()

    def __add_initial_data(self):
        def add_platform_data():
            try:
                platforms_names = [
                    'netflix',
                    'amazon video',
                    'HBO'
                ]
                for name in platforms_names:
                    Platform.create(
                        name=name
                    )
            except:
                pass
        add_platform_data()

    def __create_tables(self):
        Platform.create_table()
        Stream.create_table()
