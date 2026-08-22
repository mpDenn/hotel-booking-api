from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_open_api():
    response = client.get("/openapi.json")
    
    data = response.json()

    assert response.status_code == 200
    assert "openapi" in data
    assert "paths" in data

def test_route_not_found():
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404