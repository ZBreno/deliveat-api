from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.user import UserReq 
from repository.sqlalchemy.user import UserRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/user', tags=['User'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_user(req: UserReq, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    user = req.model_dump()
    user['id'] = uuid4()
    
    result = repo.insert_user(user)
    
    if result:
        return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create user problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_user(id: UUID, req: UserReq, sess: Session = Depends(sess_db)):
    
    user = req.model_dump(exclude_unset=True)
    repo: UserRepository = UserRepository(sess)
    
    result = repo.update_user(id, user)
    
    if result:
        return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update user error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_user(id: UUID, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.delete_user(id)
    
    if result:
        return JSONResponse(content={'message': 'user deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete user error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_user(sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_all_user()
    return result


@router.get("/get/{id}")
def get_user(id: UUID, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_user(id)
    return result