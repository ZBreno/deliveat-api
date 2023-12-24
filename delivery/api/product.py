from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.product import ProductReq
from repository.sqlalchemy.product import ProductRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/product', tags=['Product'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_product(req: ProductReq, sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    product = jsonable_encoder(req)
    product['id'] = uuid4()

    result = repo.insert_product(product)

    if result:
        return JSONResponse(content=jsonable_encoder(product), status_code=status.HTTP_201_CREATED)
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
def list_product(sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.get_all_product()
    return result


@router.get("/get/{id}")
def get_product(id: UUID, sess: Session = Depends(sess_db)):
    repo: ProductRepository = ProductRepository(sess)
    result = repo.get_product(id)
    return result
