from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.order import OrderReq
from repository.sqlalchemy.order import OrderRepository
from uuid import UUID, uuid4
from utils.generate_code import generate_code
from domain.data.sqlalchemy_models import User, Address
from datetime import datetime, timedelta
router = APIRouter(prefix='/order', tags=['Order'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_order(req: OrderReq, sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    user = sess.query(User).first()
    address = sess.query(Address).first()
    order = req.model_dump()
    order['id'] = uuid4()
    order['code'] = generate_code()
    order['user_id'] = user.id
    order['store_id'] = user.id
    order['address_id'] = address.id
    order['created_at'] = datetime.now()
    result = repo.insert_order(order)

    if result:
        return JSONResponse(content=jsonable_encoder(order), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create order problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_order(id: UUID, req: OrderReq, sess: Session = Depends(sess_db)):

    order = req.model_dump(exclude_unset=True)
    repo: OrderRepository = OrderRepository(sess)

    result = repo.update_order(id, order)

    if result:
        return JSONResponse(content=jsonable_encoder(order), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update order error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_order(id: UUID, sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    result = repo.delete_order(id)

    if result:
        return JSONResponse(content={'message': 'order deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete order error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/list")
def list_order(sess: Session = Depends(sess_db), status: str | None = None, code: str | None = None):
    user = sess.query(User).first()
    repo: OrderRepository = OrderRepository(sess=sess)
    orders = repo.get_all_order(status=status, code=code, user_id=user.id)
    
    result = []
    for order in orders:
        address = sess.query(Address).filter(Address.id == order.address_id).one_or_none()
        user = sess.query(User).filter(User.id == order.user_id).one_or_none()
        store = sess.query(User).filter(User.id == order.store_id).one_or_none()
        
        products = []
        for product in order.products:
            categories = []

            products.append({
                "name" : product.product.name,
                "description" : product.product.description,
                "cost" : product.product.cost,
                "image" : product.product.image
            })

        result.append({
            "total" : order.total,
		    "observation": order.observation,
		    "code": order.code,
		    "created_at": order.created_at,
		    "user": user.name,
		    "id": order.id,
		    "payment_method": order.payment_method,
		    "status": order.status,
		    "store": store.name,
		    "address": {
                "street" : address.street,
                "city" : address.city,
                "bumber" : address.number,
                "reference_point" : address.reference_point,
                "district" : address.district,
                "complemente" : address.complement
            },
            "products" : products
        })

    return result

@router.get("/amount")
def get_total_yesterday_and_today(sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    user = sess.query(User).first()
    result = repo.get_amount(user.id)
    return result

@router.get("/last_week")
def get_total_last_week(sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    user = sess.query(User).first()
    result = repo.get_amount_last_week(user.id)
    return result

@router.get("/count")
def get_total_last_week(sess: Session = Depends(sess_db)):
    repo: OrderRepository = OrderRepository(sess)
    user = sess.query(User).first()
    result = repo.get_count_orders(user.id)
    return result