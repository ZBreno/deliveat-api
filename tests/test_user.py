from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user/add", json={
        "name": "maria",
        "birthdate": "29/08/2004",
        "document":"321.435.453-78",
        "phone": "81028394",
        "email": "maria@gmail.com",
        "password": "senha123",
        "whatsapp": "81028394",
        "instagram": "@maria556",
        "role": "client"
        }
    )
    assert response.status_code == 200

def test_update_user():
    response = client.patch("/user/update/1", json={
        "name": "mariaaaaaaaaa",
        "birthdate": "19/08/2004",
        "document":"321.435.453-78",
        "phone": "81028394",
        "email": "maria@gmail.com",
        "password": "senha123",
        "whatsapp": "81028394",
        "instagram": "@mariad556",
        "role": "client"
        }
    )
    assert response.status_code == 200

def test_get_list_user():
    response = client.get("/user/list")
    assert response.status_code == 200

def test_get_user():
    response = client.get("/user/get/1")
    assert response.status_code == 200

def test_delete_user():
    response = client.get("/user/delete/1")
    assert response.status_code == 200

