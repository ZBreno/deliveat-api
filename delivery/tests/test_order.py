from fastapi.testclient import TestClient
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..domain.request.Order import OrderReq

from ..domain.data.sqlalchemy_models import Category, Product, User, Address, Order

from ..main import app

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

client = TestClient(app)

def test_order_model():
    client.post("/category/add", json={
        "name" : "CategoryOrder"
        }
    )
    category = session.query(Category).order_by(Category.id.desc()).first()

    client.post("/product/add", json={
        "name": "Pão com queijo",
        "description": "Pão e queijo",
        "cost": 90.99,
        "categories": category.id
        }
    )
    product = session.query(Product).order_by(Product.id.desc()).first()

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
    user = session.query(User).order_by(User.id.desc()).first()

    client.post("/address/add", json={
        "street": "Rua das flores",
        "city": "Pau dos Ferros",
        "district": "São Benedito",
        "number": "124",
        "complement": "nenhum",
        "reference_point": "nenhum",
        }
    )
    address = session.query(Address).order_by(Address.id.desc()).first()

    order = OrderReq(
        total= 35,
        observation= "Sem pepino",
        address_id= address.id,
        store_id= user.id,
        products= product.id
        )

    assert order.total == 35
    assert order.observation == "Sem pepino"
    assert order.address_id == address.id
    assert order.store_id == user.id
    assert order.products == product.id

def test_create_order():
    category = session.query(Category).order_by(Category.id.desc()).first()
    product = session.query(Product).order_by(Product.id.desc()).first()
    user = session.query(User).order_by(User.id.desc()).first()
    address = session.query(Address).order_by(Address.id.desc()).first()

    response = client.post("/order/add", json={    
        "total": 35,
        "observation": "Sem pepino",
        "address_id": address.id,
        "store_id": user.id,
        "products": product.id
        }
    )
    assert response.status_code == 201

    client.delete(f"/category/delete/{category.id}")
    client.delete(f"/address/delete/{address.id}")
    client.delete(f"/product/delete/{product.id}")
    client.delete(f"/user/delete/{user.id}")

def test_update_order():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.patch(f"/order/update/{category.id}", json={    
        "total": 38,
        "observation": "Muito pepino"
        }
    )
    assert response.status_code == 200

def test_get_list_order():
    response = client.get("/order/list")
    assert response.status_code == 200

def test_get_order():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.get(f"/order/get/{category.id}")
    assert response.status_code == 200

def test_delete_order():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.delete(f"/order/delete/{category.id}")
    assert response.status_code == 204

