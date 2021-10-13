import pytest
import random

from fastapi.testclient import TestClient

from modules.platforms.models import Platform
from modules.streams.models import Stream

from main.main import app


client = TestClient(app)


PLATFORMS_DATA_TEST = ('netflix', 'amazon video')

STREAM_DATA_TEST = ({
    "name": 'Filme 1',
    "time_paused": '03-02-30',
    "platform_id": None
}, {
    "name": 'Filme 2',
    "time_paused": '02-06-10',
    "platform_id": None
})

streams_created = []
platforms_created = []


@pytest.fixture(autouse=True)
def setUp():
    # BEFORE
    # delete streams
    for data in STREAM_DATA_TEST:
        Stream.delete().execute()

    # delete platforms
    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()

    # create create platforms
    for name in PLATFORMS_DATA_TEST:
        platform = Platform.create(name=name)
        platforms_created.append(platform)

    # create streams with post
    for data in STREAM_DATA_TEST:
        data['platform_id'] = platforms_created[0].id
        response = client.post(
            "api/stream",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json=data
        )
        data = response.json()
        assert response.status_code == 201, data['detail']
        streams_created.append(data['stream'])

    yield
    # AFTER
    # delete streams
    for data in STREAM_DATA_TEST:
        Stream.delete().execute()

    # delete platforms
    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()

    streams_created.clear()
    platforms_created.clear()


def test_update_stream_204():

    TARGET_TO_UPDATE = streams_created[0]
    TARGET_PAYLOAD = {
        "name": "Filme atualizado",
        "time_paused": "01:02:03",
        "platform_id": platforms_created[0].id
    }

    print(TARGET_PAYLOAD)

    response = client.put(
        f"api/stream/{TARGET_TO_UPDATE['id']}",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=TARGET_PAYLOAD
    )
    data = response.json()
    assert response.status_code == 204, data['detail']
    assert data == None


def test_update_stream_platform_does_not_exist_400():
    TARGET_PAYLOAD = streams_created[0]
    PLATFORM_NOT_EXIST_ID = -55
    TARGET_UPDATED = {
        "name": "Filme atualizado",
        "time_paused": "01:02:03",
        "platform_id": PLATFORM_NOT_EXIST_ID
    }

    response = client.put(
        f"api/stream/{TARGET_PAYLOAD['id']}",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=TARGET_UPDATED
    )
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == 'platform not exist'


def test_update_stream_does_not_exist_400():
    TARGET_PAYLOAD_NOT_EXIST_ID = -100
    TARGET_UPDATED = {
        "name": "Filme atualizado",
        "time_paused": "01:02:03",
        "platform_id": platforms_created[0].id
    }

    response = client.put(
        f"api/stream/{TARGET_PAYLOAD_NOT_EXIST_ID}",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=TARGET_UPDATED
    )
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == 'stream not exist'
