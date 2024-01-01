from fastapi import APIRouter, Depends, status, Form, File, UploadFile
import os
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.category import CategoryReq 
from repository.sqlalchemy.category import CategoryRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/category', tags=['Category'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_category(
    name: str = Form(...),
    image: UploadFile = File(...),
    sess: Session = Depends(sess_db)
):
    repo: CategoryRepository = CategoryRepository(sess)
    
    file_location = f"static/categories/{image.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as file_object:
        file_object.write(image.file.read())

    category_data = {
        "id": uuid4(),
        "name": name,
        "image": file_location
    }

    result = repo.insert_category(category_data)

    if result:
        return JSONResponse(content=jsonable_encoder(category_data), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create category problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_category(id: UUID, req: CategoryReq, sess: Session = Depends(sess_db)):
    
    category = req.model_dump(exclude_unset=True)
    repo: CategoryRepository = CategoryRepository(sess)
    
    result = repo.update_category(id, category)
    
    if result:
        return JSONResponse(content=jsonable_encoder(category), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update category error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_category(id: UUID, sess: Session = Depends(sess_db)):
    repo: CategoryRepository = CategoryRepository(sess)
    result = repo.delete_category(id)
    
    if result:
        return JSONResponse(content={'message': 'category deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete category error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_category(sess: Session = Depends(sess_db)):
    repo: CategoryRepository = CategoryRepository(sess)
    result = repo.get_all_category()
    return result


@router.get("/get/{id}")
def get_category(id: UUID, sess: Session = Depends(sess_db)):
    repo: CategoryRepository = CategoryRepository(sess)
    result = repo.get_category(id)
    return result