from modules.streams.models import Stream
from modules.platforms.models import Platform
from modules.users.infra.models import User


class InitData:
    def handle(self):
        self.add_platform_data()

    def add_platform_data(self):
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
                Platform.create(name=name)


class DatabaseConfig:

    __models = [Platform, Stream, User]
    __initital_data = InitData()

    def handle(self):
        self.__create_tables()
        self.__initital_data.handle()

    def __create_tables(self):
        for model in self.__models:
            model.create_table()
