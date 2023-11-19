from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import date

from domain.data.sqlalchemy_models import Address

from main import app

client = TestClient(app)

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

def test_address_model():
    address = Address(
        id = uuid4(),
        street= "Rua das flores",
        city= "Pau dos Ferros",
        district= "São Benedito",
        number= "124",
        complement= "nenhum",
        reference_point= "nenhum"
    )

    assert str(address) == f"{address.city} - {address.district} / {address.street}"

def test_create_address():
    client.post("/user/add", json={
        "name": "maria",
        "birthdate": date(2004,8,25).isoformat(),
        "document":"321.435.453-78",
        "phone": "81028394",
        "email": "maria@gmail.com",
        "password": "senha123",
        "whatsapp": "81028394",
        "instagram": "@maria556",
        "role": "client"
        }
    )
    
    response = client.post("/address/add", json={
        "street": "Rua das flores",
        "city": "Pau dos Ferros",
        "district": "São Benedito",
        "number": "124",
        "complement": "nenhum",
        "reference_point": "nenhum",
        }
    )
    assert response.status_code == 201

def test_update_address():
    address = session.query(Address).order_by(Address.id.desc()).first()

    response = client.patch(f"/address/update/{address.id}", json={
        "street": "Ruaaaa das flores",
        "city": "Pau dos Ferros",
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
    address = session.query(Address).order_by(Address.id.desc()).first()
    response = client.get(f"/address/get/{address.id}")
    assert response.status_code == 200

def test_delete_address():
    address = session.query(Address).order_by(Address.id.desc()).first()
    response = client.delete(f"/address/delete/{address.id}")
    assert response.status_code == 204

