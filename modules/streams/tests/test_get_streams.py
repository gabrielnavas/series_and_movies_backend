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
},)

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

    # create one stream
    stream_data = STREAM_DATA_TEST[0]
    stream_data['platform_id'] = platforms_created[0].id
    response = client.post(
        "api/stream",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=data
    )
    assert response.status_code == 201

    yield
    # AFTER
    # delete streams
    for data in STREAM_DATA_TEST:
        Stream.delete().execute()

    # delete platforms
    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()


def test_get_streams_200():
    response = client.get(
        f"api/stream?platform_id={platforms_created[0].id}",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data['streams']) == len(STREAM_DATA_TEST)

    assert data['streams'][0]['id'] > 0
    assert data['streams'][0]['name'] in STREAM_DATA_TEST[0]['name']
    assert data['streams'][0]['time_paused'] in \
        STREAM_DATA_TEST[0]['time_paused'].replace('-', ':')
