from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_category():
    response = client.post("/category/add", json={
        "name" : "Massas"
        }
    )
    assert response.status_code == 200

def test_update_category():
    response = client.patch("/category/update/1", json={
        "name" : "Massas secas"
        }
    )
    assert response.status_code == 200

def test_get_list_category():
    response = client.get("/category/list")
    assert response.status_code == 200

def test_get_category():
    response = client.get("/category/get/1")
    assert response.status_code == 200

def test_delete_category():
    response = client.get("/category/delete/1")
    assert response.status_code == 200

