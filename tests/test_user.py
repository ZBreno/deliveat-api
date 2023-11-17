from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from domain.request.user import UserReq

from domain.data.sqlalchemy_models import User

from main import app
from datetime import date

client = TestClient(app)

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

def test_user_model():
    user = User(
        name="maria", 
        birthdate=date(2004,8,25).isoformat(), 
        document="321.435.453-78", 
        phone="81028394",
        email = "maria@gmail.com",
        password= "senha123",
        whatsapp= "81028394",
        instagram= "@maria556",
        role= "client")

    assert str(user) == user.name

def test_create_user():
    response = client.post("/user/add", json={
        "name": "maria",
        "birthdate": date(2004,8,25).isoformat(),
        "document":"329.435.453-78",
        "phone": "11008673",
        "email": "mariaaiii@gmail.com",
        "password": "senha123",
        "whatsapp": "81259544",
        "instagram": "@mariaoi556",
        "role": "client"
        }
    )
    assert response.status_code == 201

def test_update_user():
    user = session.query(User).order_by(User.id.desc()).first()
    response = client.patch(f"/user/update/{user.id}", json={
        "name": "mariaaaaaaaaa",
        "birthdate": date(2004,8,25).isoformat(),
        "document":"321.435.453-78",
        "phone": "81028394",
        "email": "maria@gmail.com",
        "password": "senha123",
        "whatsapp": "85027385",
        "instagram": "@madriad556",
        "role": "client"
        }
    )
    assert response.status_code == 200

def test_get_list_user():
    response = client.get("/user/list")
    assert response.status_code == 200

def test_get_user():
    user = session.query(User).order_by(User.id.desc()).first()
    response = client.get(f"/user/get/{user.id}")
    assert response.status_code == 200

def test_delete_user():
    user = session.query(User).order_by(User.id.desc()).first()
    response = client.delete(f"/user/delete/{user.id}")
    assert response.status_code == 204
    user = session.query(User).order_by(User.id.desc()).first()
    response = client.delete(f"/user/delete/{user.id}")

