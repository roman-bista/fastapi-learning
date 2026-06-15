from fastapi.testclient import TestClient
from TodoApp.main import app
  
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}


