from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.user import UserReq
from domain.data.sqlalchemy_models import User
from repository.sqlalchemy.user import UserRepository
from uuid import UUID
from security.secure import get_current_user

router = APIRouter(prefix='/user', tags=['User'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

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

@router.get("/me")
def read_current_user(current_user: str = Depends(get_current_user), sess: Session = Depends(sess_db)):
    print(current_user)
    repo: UserRepository = UserRepository(sess)
    user = repo.get_user_me(current_user)

    if user:
        return user
    else:
        return JSONResponse(content={'message': 'User not found'}, status_code=status.HTTP_404_NOT_FOUND)