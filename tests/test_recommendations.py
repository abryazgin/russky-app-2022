from fastapi.testclient import TestClient

from russky.app import app

client = TestClient(app)


def test_read_main():
    response = client.get('/api/random')
    assert response.status_code == 200
