from fastapi.testclient import TestClient
from datetime import date
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from domain.data.sqlalchemy_models import Category, Product, User, Address, Order

from main import app

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
        "cost": 90,
        "categories": [],
        "products_bonus": []
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

    order = Order(
        total= 35,
        observation= "Sem pepino",
        address_id= jsonable_encoder(address),
        store_id= jsonable_encoder(user),
        products= [jsonable_encoder(product)]
        )

    assert str(order) == f"{order.user_id} / {order.total}"

def test_create_order():
    category = session.query(Category).order_by(Category.id.desc()).first()
    client.post("/product/add", json={
        "name": "Pão com queijo",
        "description": "Pão e queijo",
        "cost": 90,
        "categories": [],
        "products_bonus": []
        }
    )
    product = session.query(Product).order_by(Product.id.desc()).first()
    user = session.query(User).order_by(User.id.desc()).first()
    address = session.query(Address).order_by(Address.id.desc()).first()
    print(category, product, user, address)

    response = client.post("/order/add", json={    
        "total": 35,
        "observation": "Sem pepino",
        "address_id": jsonable_encoder(address),
        "store_id": jsonable_encoder(user),
        "products": [jsonable_encoder(product)]
        }
    )
    assert response.status_code == 201

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

