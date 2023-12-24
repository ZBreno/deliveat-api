from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from domain.data.sqlalchemy_models import Category

from main import app

client = TestClient(app)

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

def test_category_model():
    category = Category(
        name = "Massas" )

    assert str(category) == "Massas"

def test_create_category():
    response = client.post("/category/add", json={
        "name" : "Massas"
        }
    )
    assert response.status_code == 201

def test_update_category():
    category = session.query(Category).order_by(Category.id.desc()).first()

    response = client.patch(f"/category/update/{category.id}", json={
        "name" : "Massas secas"
        }
    )
    assert response.status_code == 200

def test_get_list_category():
    response = client.get("/category/list")
    assert response.status_code == 200

def test_get_category():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.get(f"/category/get/{category.id}")
    assert response.status_code == 200

def test_delete_category():
    category = session.query(Category).order_by(Category.id.desc()).first()
    response = client.delete(f"/category/delete/{category.id}")
    assert response.status_code == 204

