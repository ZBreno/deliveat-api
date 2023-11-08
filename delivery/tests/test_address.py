from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_address():
    response = client.post("/address/add", json={
        "street": "Rua das flores",
        "city": "Pau dos Ferros",
        "district": "São Benedito",
        "number": "124",
        "complement": "nenhum",
        "reference_point": "nenhum",
        }
    )
    assert response.status_code == 200

def test_update_address():
    response = client.patch("/address/update/1", json={
        "street": "Ruaaaa das flores",
        "city": "Paua dos Ferros",
        "district": "São Benedito",
        "number": "124",
        "complement": "nenhum",
        "reference_point": "nenhum",
        }
    )
    assert response.status_code == 200

def test_get_list_address():
    response = client.get("/address/list")
    assert response.status_code == 200

def test_get_address():
    response = client.get("/address/get/1")
    assert response.status_code == 200

def test_delete_address():
    response = client.get("/address/delete/1")
    assert response.status_code == 200

