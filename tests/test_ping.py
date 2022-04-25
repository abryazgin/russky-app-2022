from fastapi.testclient import TestClient

from russky.app import app

client = TestClient(app)


def test_read_main():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == 'OK'
