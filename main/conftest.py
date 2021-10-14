from main.database_config import DatabaseConfig


# execute before all tests
def pytest_configure(config):
    database_config = DatabaseConfig()
    database_config.handle()
