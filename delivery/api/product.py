from fastapi import APIRouter, Depends, status, Form, File, UploadFile
import os
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.product import ProductReq
from repository.sqlalchemy.product import ProductRepository
from repository.sqlalchemy.user import UserRepository
from security.secure import get_current_user
from uuid import UUID, uuid4
from typing import List

router = APIRouter(prefix='/product', tags=['Product'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_product(
    name: str = Form(...),
    description: str = Form(...),
    cost: float = Form(...),
    image: UploadFile = File(...),
    categories: List[str] = Form(...),
    products_bonus: List[str] = Form(default=[]),
    sess: Session = Depends(sess_db),
    current_user: str = Depends(get_current_user)
):
    repo: UserRepository = UserRepository(sess)
    user = repo.get_user_me(current_user)
    repo: ProductRepository = ProductRepository(sess)

    file_location = f"static/uploads/{image.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as file_object:
        file_object.write(image.file.read())

    product_data = {
        "id": uuid4(),
        "name": name,
        "description": description,
        "cost": cost,
        "image": file_location,
        "categories": categories,
        "products_bonus": products_bonus,
        "user_id": user.id,
    }

    result = repo.insert_product(product_data)

    if result:
        return JSONResponse(content=jsonable_encoder(product_data), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create product problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_product(id: UUID, req: ProductReq, sess: Session = Depends(sess_db)):

    product = req.model_dump(exclude_unset=True)
    repo: ProductRepository = ProductRepository(sess)

    result = repo.update_product(id, product)

    if result:
        return JSONResponse(content=jsonable_encoder(product), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update product error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_product(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.delete_product(id)

    if result:
        return JSONResponse(content={'message': 'product deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete product error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_product(sess: Session = Depends(sess_db), category: str | None = None):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.get_all_product(category=category)
    return result


@router.get("/list/products_store/{id}")
def get_product(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.get_my_products(id)
    return result


@router.get("/get/{id}")
def get_product(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.get_product(id)
    return result
