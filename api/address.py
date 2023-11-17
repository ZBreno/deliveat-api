from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.address import AddressReq 
from repository.sqlalchemy.address import AddressRepository
from domain.data.sqlalchemy_models import User
from uuid import UUID, uuid4

router = APIRouter(prefix='/address', tags=['Address'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
async def add_address(req: AddressReq, sess: Session = Depends(sess_db)):
    user = sess.query(User).order_by(User.id.desc()).first()

    repo: AddressRepository = AddressRepository(sess)
    address = req.model_dump()
    address['id'] = uuid4()
    address['user_id'] = user.id
    
    result = repo.insert_address(address)
    
    if result:
        return JSONResponse(content=jsonable_encoder(address), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create address problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
async def update_address(id: UUID, req: AddressReq, sess: Session = Depends(sess_db)):
    
    address = req.model_dump(exclude_unset=True)
    repo: AddressRepository = AddressRepository(sess)
    
    result = repo.update_address(id, address)
    
    if result:
        return JSONResponse(content=jsonable_encoder(address), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update address error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
async def delete_address(id: UUID, sess: Session = Depends(sess_db)):
    repo: AddressRepository = AddressRepository(sess)
    result = repo.delete_address(id)
    
    if result:
        return JSONResponse(content={'message': 'address deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete address error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
async def list_address(sess: Session = Depends(sess_db)):
    repo: AddressRepository = AddressRepository(sess)
    result = repo.get_all_address()
    return result


@router.get("/get/{id}")
async def get_address(id: UUID, sess: Session = Depends(sess_db)):
    repo: AddressRepository = AddressRepository(sess)
    result = repo.get_address(id)
    return result