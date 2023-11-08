from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.order import OrderReq 
from repository.sqlalchemy.order import OrderRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/order', tags=['Order'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
async def add_order(req: OrderReq, sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    order = req.model_dump()
    order['id'] = uuid4()
    
    result = repo.insert_order(order)
    
    if result:
        return JSONResponse(content=jsonable_encoder(order), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create order problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
async def update_order(id: UUID, req: OrderReq, sess: Session = Depends(sess_db)):
    
    order = req.model_dump(exclude_unset=True)
    repo: OrderRepository = OrderRepository(sess)
    
    result = repo.update_order(id, order)
    
    if result:
        return JSONResponse(content=jsonable_encoder(order), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update order error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
async def delete_order(id: UUID, sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    result = repo.delete_order(id)
    
    if result:
        return JSONResponse(content={'message': 'order deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete order error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
async def list_order(sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    result = repo.get_all_order()
    return result


@router.get("/get/{id}")
async def get_order(id: UUID, sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    result = repo.get_order(id)
    return result