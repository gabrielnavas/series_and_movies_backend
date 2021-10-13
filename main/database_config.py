from modules.streams.models import Stream
from modules.platforms.models import Platform
from main.env import ENV_NOW, DEV


class DatabaseConfig:
    is_create_table = ENV_NOW != DEV

    def handle(self):
        self.__create_tables()
        if not self.is_create_table:
            self.__add_initial_data()

    def __add_initial_data(self):
        def add_platform_data():
            platforms_names = [
                'netflix',
                'amazon video',
                'HBO'
            ]
            for name in platforms_names:
                platforms_founds = (
                    Platform
                    .select()
                    .where(Platform.name == name)
                )
                if len(platforms_founds) == 0:
                    Platform.create(
                        name=name
                    )
        add_platform_data()

    def __create_tables(self):
        Platform.create_table()
        Stream.create_table()
