from datetime import datetime
from fastapi.testclient import TestClient
import pytest

from modules.users.infra.models import User

from main.main import app


client = TestClient(app)

fake_email = "julio@gmail.com"
fake_password = "123456"


def create_user_login_test_OK():
    return {
        "email": fake_email,
        "password": fake_password,
    }


def create_user_test_OK():
    return {
        "first_name": "Julio",
        "last_name": "Silva",
        "email": fake_email,
        "password": fake_password,
        "password_confirmation": fake_password,
    }


@pytest.fixture(autouse=True)
def setUp():
    # BEFORE
    yield
    # AFTER
    User.delete().execute()


def test_create_user_201():

    def __create_user(user_test_data):
        response = client.post(
            "api/user",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=user_test_data
        )
        data = response.json()

        assert response.status_code == 201
        return data['user']

    user_test_data = create_user_test_OK()
    user_test_data_login = create_user_login_test_OK()
    __create_user(user_test_data)

    response = client.post(
        "api/user/login",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=user_test_data_login
    )
    data = response.json()

    assert response.status_code == 201

    # user
    user = data['user']
    assert len(user.items()) == 5, 'should be 5 items'
    assert user['id'] > 0
    assert datetime.fromisoformat(user['created_at']).date()
    assert user['first_name'] == user_test_data['first_name']
    assert user['last_name'] == user_test_data['last_name']
    assert user['email'] == user_test_data['email']

    # token
    token = data['token']
    assert len(token) > 0


def test_email_wrong_user_400():
    def __create_user():
        user_test_data = create_user_test_OK()
        response = client.post(
            "api/user",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=user_test_data
        )
        data = response.json()

        assert response.status_code == 201
        return data['user']

    user_test_data = __create_user()
    user_test_data = create_user_login_test_OK()
    user_test_data['email'] = 'wrong_email'

    response = client.post(
        "api/user/login",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=user_test_data
    )
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'user does not exist'


def test_email_doesnt_exist_user_400():
    def __create_user():
        user_test_data = create_user_test_OK()
        response = client.post(
            "api/user",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=user_test_data
        )
        data = response.json()

        assert response.status_code == 201
        return data['user']

    def __try_login(user_created):
        user_test_data = create_user_login_test_OK()
        user_test_data['email'] = 'wrong_email@email.com'

        response = client.post(
            "api/user/login",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=user_test_data
        )
        data = response.json()

        assert response.status_code == 400
        assert data['detail'] == 'user does not exist'

    user = __create_user()
    __try_login(user)


def test_password_doesnt_exist_user_400():
    def __create_user():
        user_test_data = create_user_test_OK()
        response = client.post(
            "api/user",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=user_test_data
        )
        data = response.json()

        assert response.status_code == 201
        return data['user']

    user_test_data = __create_user()
    user_test_data = create_user_login_test_OK()
    user_test_data['password'] = 'wrong_password'

    response = client.post(
        "api/user/login",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=user_test_data
    )
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'user does not exist'
