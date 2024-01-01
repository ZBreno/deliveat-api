from fastapi import APIRouter, Depends, status, Form, File, UploadFile
import os
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.product_bonus import ProductBonusReq
from repository.sqlalchemy.product_bonus import ProductBonusRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/product_bonus', tags=['Product Bonus'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_product_bonus(
    name: str = Form(...),
    description: str = Form(...),
    cost: float = Form(...),
    image: UploadFile = File(...),
    sess: Session = Depends(sess_db)
):
    repo: ProductBonusRepository = ProductBonusRepository(sess)

    file_location = f"static/uploads/{image.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as file_object:
        file_object.write(image.file.read())

    product_bonus_data = {
        "id": uuid4(),
        "name": name,
        "description": description,
        "cost": cost,
        "image": file_location
    }

    result = repo.insert_product_bonus(product_bonus_data)

    if result:
        return JSONResponse(content=jsonable_encoder(product_bonus_data), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create product_bonus problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_product_bonus(id: UUID, req: ProductBonusReq, sess: Session = Depends(sess_db)):
    
    product_bonus = req.model_dump(exclude_unset=True)
    repo: ProductBonusRepository = ProductBonusRepository(sess)
    
    result = repo.update_product_bonus(id, product_bonus)
    
    if result:
        return JSONResponse(content=jsonable_encoder(product_bonus), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update product_bonus error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_product_bonus(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductBonusRepository = ProductBonusRepository(sess)
    result = repo.delete_product_bonus(id)
    
    if result:
        return JSONResponse(content={'message': 'product_bonus deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete product_bonus error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_product_bonus(sess: Session = Depends(sess_db)):
    repo: ProductBonusRepository = ProductBonusRepository(sess)
    result = repo.get_all_product_bonus()
    return result


@router.get("/get/{id}")
def get_product_bonus(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductBonusRepository = ProductBonusRepository(sess)
    result = repo.get_product_bonus(id)
    return result