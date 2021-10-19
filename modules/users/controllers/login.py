from typing import Any
from fastapi import APIRouter, status, Response, Request
from pydantic import BaseModel

from modules.users.usecases.login import LoginUsecase, LoginValidation
from modules.users.usecases.exceptions import ExceptionUser
from modules.shared.infra.errors_handler import LogHttpErrorHandler

router = APIRouter()


class LoginBody(BaseModel):
    email: str
    password: str


@router.post("/api/user/login")
async def login(user_body: LoginBody, request: Request, response: Response):
    try:
        validation = LoginValidation()
        validation.validate(user_body.email, user_body.password)

        login_usecase = LoginUsecase()
        result_usecase = login_usecase.login(
            user_body.email, user_body.password)
        delattr(result_usecase.user, 'password')
        response.status_code = status.HTTP_201_CREATED
        return {
            "user": result_usecase.user,
            "token": result_usecase.token
        }
    except ExceptionUser as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(e)}
    except Exception as e:
        error_handler = LogHttpErrorHandler()
        error_handler.handle(
            request=request,
            response=response,
            body=user_body,
            error=e
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f'server error'}
