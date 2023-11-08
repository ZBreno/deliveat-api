from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_ticket():
    response = client.post("/ticket/add", json={
        "deadline": "2023-11-08",
        "code": "#BOATARDE",
        "description": "30% de desconto em compras acima de R$20",
        "type": "socorro"
        }
    )
    assert response.status_code == 200

def test_update_ticket():
    response = client.patch("/ticket/update/1", json={
        "deadline": "2023-11-08",
        "code": "#BOTARDE",
        "description": "50% de desconto em compras acima de R$20",
        "type": "socdorro"
        }
    )
    assert response.status_code == 200

def test_get_list_ticket():
    response = client.get("/ticket/list")
    assert response.status_code == 200

def test_get_ticket():
    response = client.get("/ticket/get/1")
    assert response.status_code == 200

def test_delete_ticket():
    response = client.get("/ticket/delete/1")
    assert response.status_code == 200

