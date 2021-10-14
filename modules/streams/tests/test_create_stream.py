from fastapi.testclient import TestClient
import pytest

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
        Platform.create(name=name)

    yield
    # AFTER

    for data in STREAM_DATA_TEST:
        Stream.delete().execute()

    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()


def get_platforms():
    response = client.get("/api/platform")
    data = response.json()
    return data['platforms']


def test_create_stream_201():
    platforms = get_platforms()

    stream_test_data = STREAM_DATA_TEST[0]
    stream_test_data['platform_id'] = platforms[0]['id']

    response = client.post(
        "api/stream",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=stream_test_data
    )
    data = response.json()

    assert response.status_code == 201
    assert data['stream']['id'] > 0
    assert data['stream']['name'] in stream_test_data['name']
    assert data['stream']['time_paused'] in \
        stream_test_data['time_paused'].replace('-', ':')


def test_create_stream_platform_doest_exist_400():
    platforms = get_platforms()

    stream_test_data = STREAM_DATA_TEST[0]
    stream_test_data['platform_id'] = -500

    response = client.post(
        "api/stream",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=stream_test_data
    )
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'platform does not exist'


def test_create_stream_stream_already_exists_400():

    # add one stream before
    test_create_stream_201()

    # test second stream with equals name
    platforms = get_platforms()

    stream_test_data = STREAM_DATA_TEST[0]
    stream_test_data['platform_id'] = platforms[0]['id']

    response_stream2 = client.post(
        "api/stream",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=stream_test_data
    )
    data_stream2 = response_stream2.json()

    assert response_stream2.status_code == 400
    assert data_stream2['detail'] == 'Stream já existe na plataforma.'
