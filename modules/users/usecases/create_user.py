from typing import List, Dict, Any
import re

from modules.users.infra.password_hash import BcryptHash
from modules.users.infra.user_repository import UserRepositoy
from modules.users.usecases.models import UserValidationModel, UserModel

from .exceptions import ExceptionUser


class UserValidation:
    __email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def validate(self, user: UserValidationModel) -> List[str]:
        if len(user.first_name) < 2 or len(user.first_name) > 180:
            raise ExceptionUser(
                'first name need to be between 2 and 100 character')

        if len(user.last_name) < 2 or len(user.last_name) > 100:
            raise ExceptionUser(
                'last name need to be between 2 and 100 character')

        if not re.fullmatch(self.__email_regex, user.email):
            raise ExceptionUser('emails is wrong')

        if len(user.password) < 6 or len(user.password) > 100:
            raise ExceptionUser(
                'password need to be between 7 and 100 character')

        if len(user.password_confirmation) < 6 or len(user.password_confirmation) > 100:
            raise ExceptionUser(
                'password confirmation need to be between 7 and 100 character')

        if user.password != user.password_confirmation:
            raise ExceptionUser(
                'password is different of password confirmation')


class DbCreateUserUsecase:
    def __init__(self,
                 hash_password: BcryptHash = BcryptHash(),
                 user_repository: UserRepositoy = UserRepositoy()):
        self.hash_password = hash_password
        self.user_repository = user_repository

    def create(self, user: UserValidationModel) -> UserModel:
        user_found = self.user_repository.search_by_email(user.email)
        if user_found:
            raise ExceptionUser('user has exists with email')

        password_hashed = self.hash_password.create(user.password)
        user.password = password_hashed
        user_created = self.user_repository.create(user)
        return user_created
