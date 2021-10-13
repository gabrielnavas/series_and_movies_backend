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
