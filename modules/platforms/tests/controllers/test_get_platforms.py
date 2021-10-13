from fastapi.testclient import TestClient
import pytest

from modules.platforms.models import Platform
from main.main import app


client = TestClient(app)

PLATFORMS_DATA_TEST = ('netflix', 'amazon video', 'HBO')


@pytest.fixture(autouse=True)
def setUp():
    # BEFORE
    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()

    for name in PLATFORMS_DATA_TEST:
        Platform.create(name=name)

    yield

    # AFTER
    for name in PLATFORMS_DATA_TEST:
        Platform.delete().execute()


def test_get_all_platforms():
    response = client.get("/api/platform")
    data = response.json()
    assert response.status_code == 200
    assert len(data['platforms']) == 3
    for platform in data['platforms']:
        assert platform['id'] > 0
        assert platform['name'] in PLATFORMS_DATA_TEST
