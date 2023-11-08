from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_rating():
    response = client.post("/rating/add", json={
        "rating": 5,
        "description": "Gostei",
        "user_id": 1,
        "order_id": 1
        }
    )
    assert response.status_code == 200

def test_update_rating():
    response = client.patch("/rating/update/1", json={
        "rating": 4,
        "description": "Gostei muito",
        "user_id": 1,
        "order_id": 1
        }
    )
    assert response.status_code == 200

def test_get_list_rating():
    response = client.get("/rating/list")
    assert response.status_code == 200

def test_get_rating():
    response = client.get("/rating/get/1")
    assert response.status_code == 200

def test_delete_rating():
    response = client.get("/rating/delete/1")
    assert response.status_code == 200

