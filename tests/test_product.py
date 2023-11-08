from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/product/add", json={
        "name": "Pão com queijo",
        "description": "Pão e queijo",
        "cost": 90.99,
        "categories": [1]
        }
    )
    assert response.status_code == 200

def test_update_product():
    response = client.patch("/product/update/1", json={
        "name": "Pão com queijo e bolo",
        "description": "Pão e queijo + bolo",
        "cost": 90.99,
        "categories": [1]
        }
    )
    assert response.status_code == 200

def test_get_list_product():
    response = client.get("/product/list")
    assert response.status_code == 200

def test_get_product():
    response = client.get("/product/get/1")
    assert response.status_code == 200

def test_delete_product():
    response = client.get("/product/delete/1")
    assert response.status_code == 200

