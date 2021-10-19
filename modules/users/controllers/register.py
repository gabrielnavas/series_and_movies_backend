from fastapi import APIRouter, status, Response
from pydantic import BaseModel

from modules.users.usecases.create_user import UserValidationModel, UserValidation, DbCreateUserUsecase
from modules.users.usecases.exceptions import ExceptionUser

router = APIRouter()


class UserBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    password_confirmation: str


@router.post("/api/user")
async def create_user(user_body: UserBody, response: Response):
    try:
        user = UserValidationModel(
            first_name=user_body.first_name,
            last_name=user_body.last_name,
            email=user_body.email,
            password=user_body.password,
            password_confirmation=user_body.password_confirmation,
        )
        validation = UserValidation()
        validation.validate(user)

        db_create_user = DbCreateUserUsecase()
        user = db_create_user.create(user)
        del user['password']
        response.status_code = status.HTTP_201_CREATED
        return {
            "user": user
        }
    except ExceptionUser as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": 'server error'}
