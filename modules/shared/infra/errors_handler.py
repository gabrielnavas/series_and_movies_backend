from typing import Any
from uuid import uuid4
import json
import pprint

from fastapi import Request, Response
from modules.shared.models import BaseModel, peewee
from main.env import CREATE_LOG_DATABASE, LOG_ERROR_ON_CONSOLE


class LogHTTPError(BaseModel):
    id = peewee.UUIDField(default=uuid4)

    request_url = peewee.CharField(max_length=1000)
    request_headers = peewee.CharField(max_length=1000)
    request_path_params = peewee.CharField(max_length=1000)
    request_query_params = peewee.CharField(max_length=1000)
    request_body_params = peewee.CharField(max_length=1000)

    response_status_code = peewee.IntegerField()
    response_headers = peewee.CharField(max_length=1000)
    response_body_params = peewee.CharField(max_length=1000)

    error_exception = peewee.CharField(max_length=1000)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LogHttpErrorHandler:
    is_create_log_database = CREATE_LOG_DATABASE
    is_log_on_console = LOG_ERROR_ON_CONSOLE

    def handle(self, request: Request, response: Response, error: Exception, body: Any = {}):
        print(self.is_create_log_database)
        print(self.is_log_on_console)
        if self.is_create_log_database:
            self.__create_log(request, response, body, error)

        if self.is_log_on_console:
            self.__log_on_console(request, response, body, error)

    def __log_on_console(self, request: Request, response: Response, body: Any, error: Exception):
        payload = {
            "request": {
                'url': str(request.url),
                'headers': dict(request.headers),
                'path params': dict(request.path_params),
                'query params': dict(request.query_params),
                'body params': dict(body),
            },
            "response": {
                'status code': response.status_code,
                'headers': dict(response.headers),
                'body params': dict(response.body),
                'error exception': error.__str__(),
            }
        }
        print(bcolors.UNDERLINE + '_' * 79 + bcolors.ENDC)
        print(bcolors.HEADER + bcolors.FAIL)
        pprint.PrettyPrinter(indent=4, width=41).pprint(payload)
        print(bcolors.ENDC + bcolors.UNDERLINE + '_' * 79 + bcolors.ENDC)

    def __create_log(self,  request: Request, response: Response, body: Any, error: Exception):
        error = LogHTTPError.create(
            request_url=request.url.__str__(),
            request_headers=json.dumps(dict(request.headers)),
            request_path_params=json.dumps(dict(request.path_params)),
            request_query_params=json.dumps(dict(request.query_params)),
            request_body_params=json.dumps(dict(body)),

            response_status_code=response.status_code,
            response_headers=json.dumps(dict(response.headers)),
            response_body_params=json.dumps(dict(response.body)),

            error_exception=json.dumps(error.__str__()),
        )


def create_tables():
    tables = [
        ('LogError', LogError),
    ]
    for table in tables:
        print(f'Creating table {table[0]}')
        table[1].create_table()
