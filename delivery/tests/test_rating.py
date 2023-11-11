from fastapi.testclient import TestClient
from datetime import date
from ..domain.request.Rating import RatingReq
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..domain.data.sqlalchemy_models import Category, Product, User,Address, Rating, Order

from ..main import app

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

client = TestClient(app)

def test_rating_model():
    client.post("/category/add", json={
        "name" : "CategoryOrder"
        }
    )
    category = session.query(Category).order_by(Category.id.desc()).first()

    client.post("/product/add", json={
        "name": "Pão com queijo",
        "description": "Pão e queijo",
        "cost": 90.99,
        "categories": [category.id]
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
    
    client.post("/order/add", json={    
        "total": 35,
        "observation": "Sem pepino",
        "address_id": address.id,
        "store_id": user.id,
        "products": product.id
        }
    )
    order = session.query(Order).order_by(Order.id.desc()).first()

    rating = RatingReq(
        rating = 5,
        description = "Gostei",
        user_id = user.id,
        order_id = order.id)

    assert rating.rating == 5
    assert rating.description == "Gostei"
    assert rating.user_id == user.id
    assert rating.order_id == order.id

def test_create_rating():
    order = session.query(Order).order_by(Order.id.desc()).first()
    user = session.query(User).order_by(User.id.desc()).first()
    
    response = client.post("/rating/add", json={
        "rating": 5,
        "description": "Gostei",
        "user_id": user.id,
        "order_id": order.id
        }
    )
    assert response.status_code == 201

def test_update_rating():
    rating = session.query(Rating).order_by(Rating.id.desc()).first()
    
    response = client.patch(f"/rating/update/{rating.id}", json={
        "rating": 4,
        "description": "Gostei muito"
        }
    )
    assert response.status_code == 200

def test_get_list_rating():
    response = client.get("/rating/list")
    assert response.status_code == 200

def test_get_rating():
    rating = session.query(Rating).order_by(Rating.id.desc()).first()
    response = client.get(f"/rating/get/{rating.id}")
    assert response.status_code == 200

def test_delete_rating():
    rating = session.query(Rating).order_by(Rating.id.desc()).first()
    response = client.delete(f"/rating/delete/{rating.id}")
    assert response.status_code == 204

