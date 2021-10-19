from typing import List
import re


from modules.users.usecases.models import UserModel
from modules.users.usecases.exceptions import ExceptionUser

from modules.users.infra.password_hash import BcryptHash
from modules.users.infra.jwt_hash import JwtCrypter
from modules.users.infra.user_repository import UserRepositoy

from email_validator import validate_email, EmailNotValidError


class UserValidation:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class LoginValidation:

    def validate(self, email: str, password: str) -> List[str]:
        try:
            validate_email(email)
        except EmailNotValidError as e:
            print(str(e))
            raise ExceptionUser('user does not exist')

        if len(password) < 6 or len(password) > 100:
            raise ExceptionUser(
                'password need to be between 7 and 100 character')


class LoginResponse:
    def __init__(self, token: str, user: UserModel):
        self.token = token
        self.user = user


class LoginUsecase:
    def __init__(
            self,
            hash_password: BcryptHash = BcryptHash(),
            create_token: JwtCrypter = JwtCrypter(),
            user_repository: UserRepositoy = UserRepositoy()):
        self.hash_password = hash_password
        self.token = create_token
        self.user_repository = user_repository

    def login(self, email: str, plain_password: str) -> LoginResponse:
        user_found = self.user_repository.search_by_email(
            email=email)

        if not user_found:
            raise ExceptionUser('user does not exist')

        if not self.hash_password.check(
                plain_password=plain_password,
                hash_password=user_found['password']):
            raise ExceptionUser('user does not exist')
        payload = {'user_id': user_found['id']}
        token = self.token.create(payload)
        user = UserModel(
            id=user_found['id'],
            first_name=user_found['first_name'],
            last_name=user_found['last_name'],
            email=user_found['email'],
            password=user_found['password'],
            created_at=user_found['created_at']
        )
        return LoginResponse(token, user)
