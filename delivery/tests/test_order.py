from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_create_order():
    response = client.post("/order/add", json={    
        "total": 35,
        "observation": "Sem pepino",
        "address_id": 1,
        "store_id": 1,
        "user_id": 1 
        }
    )
    assert response.status_code == 200

def test_update_order():
    response = client.patch("/order/update/1", json={    
        "total": 38,
        "observation": "Muito pepino",
        "address_id": 1,
        "store_id": 1,
        "user_id": 1 
        }
    )
    assert response.status_code == 200

def test_get_list_order():
    response = client.get("/order/list")
    assert response.status_code == 200

def test_get_order():
    response = client.get("/order/get/1")
    assert response.status_code == 200

def test_delete_order():
    response = client.get("/order/delete/1")
    assert response.status_code == 200

