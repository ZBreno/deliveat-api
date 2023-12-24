from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Product, Category

from main import app

client = TestClient(app)

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

def test_product_model():
    client.post("/category/add", json={
        "name" : "BOLOS"
        }
    )
    category = session.query(Category).order_by(Category.id.desc()).first()
    
    product = Product(
        name = "Pão com queijo",
        description = "Pão e queijo",
        cost = 90.99,
        categories = [category]
    )

    assert str(product) == product.name

def test_create_product():
    category = session.query(Category).order_by(Category.id.desc()).first()

    response = client.post("/product/add", json={
        "name": "Pão com queijo",
        "description": "Pão e queijo",
        "cost": 90.99,
        "categories": category.id
        }
    )
    assert response.status_code == 201

def test_update_product():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.patch(f"/product/update/{category.id}", json={
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
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.get(f"/product/get/{category.id}")
    assert response.status_code == 200

def test_delete_product():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.delete(f"/product/delete/{category.id}")
    assert response.status_code == 204

