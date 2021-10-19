from datetime import datetime
from fastapi.testclient import TestClient
import pytest

from modules.users.infra.models import User

from main.main import app


client = TestClient(app)


def create_user_test_OK():
    return {
        "first_name": "Julio",
        "last_name": "Silva",
        "email": "julio@email.com",
        "password": "123456",
        "password_confirmation": "123456",
    }


@pytest.fixture(autouse=True)
def setUp():
    # BEFORE

    yield
    # AFTER
    User.delete().execute()


def test_create_user_201():
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
    assert len(data['user'].items()) == 5, 'should be 5 items'
    assert data['user']['id'] > 0
    assert datetime.fromisoformat(data['user']['created_at']).date()
    assert data['user']['first_name'] == user_test_data['first_name']
    assert data['user']['last_name'] == user_test_data['last_name']
    assert data['user']['email'] == user_test_data['email']


def test_error_user_400():
    user_test_data = create_user_test_OK()
    user_test_data['first_name'] = 'a'

    response = client.post(
        "api/user",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=user_test_data
    )
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'first name need to be between 2 and 100 character'


def test_create_user_already_exists_400():
    user_test_data = create_user_test_OK()

    def _create_first_user(user_test_data):
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

    _create_first_user(user_test_data)
    response = client.post(
        "api/user",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=user_test_data
    )
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'user has exists with email'
