from typing import Union
from .models import User as UserPeewee
from modules.users.usecases.models import UserValidationModel
from playhouse.shortcuts import model_to_dict


class UserRepositoy:
    def search_by_email(self, email: str) -> Union[UserPeewee, None]:
        try:
            user = UserPeewee.get(UserPeewee.email == email)
            return model_to_dict(user)
        except Exception as ex:
            return None

    def create(self, user: UserValidationModel) -> UserPeewee:
        user_created = UserPeewee.create(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
        )
        return model_to_dict(user_created)
