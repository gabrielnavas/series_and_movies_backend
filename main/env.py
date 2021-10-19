import os

try:
    HEROKU_DATABASE_URL = os.environ['DATABASE_URL']
except:
    HEROKU_DATABASE_URL = None

try:
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'
    ENV_NOW = os.environ['ENV']
except:
    ENV_NOW = None


try:
    CREATE_LOG_DATABASE = os.environ['CREATE_LOG_DATABASE']
    LOG_ERROR_ON_CONSOLE = os.environ['LOG_ERROR_ON_CONSOLE']
except:
    CREATE_LOG_DATABASE = None
    LOG_ERROR_ON_CONSOLE = None
