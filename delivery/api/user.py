from fastapi import APIRouter, Depends, status, UploadFile, File, Form
import os
from fastapi.responses import JSONResponse
from datetime import date
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.user import UserReq, UpdateUserReq
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
def update_user(
    id: UUID,
    name: Optional[str] = Form(None),
    birthdate: Optional[date] = Form(None),
    document: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    instagram: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    delivery_cost: Optional[float] = Form(None),
    time_prepare: Optional[str] = Form(None),
    profile_picture: UploadFile = File(None),
    sess: Session = Depends(sess_db)
):
    repo: UserRepository = UserRepository(sess)
    existing_user = repo.get_user(id)

    if profile_picture:
        file_location = f"static/uploads/{profile_picture.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as file_object:
            file_object.write(profile_picture.file.read())
        existing_user.profile_picture = file_location

    user_data = {
        "name": name or existing_user.name,
        "birthdate": birthdate or existing_user.birthdate,
        "document": document or existing_user.document,
        "phone": phone or existing_user.phone,
        "email": email or existing_user.email,
        "password": password or existing_user.password,
        "instagram": instagram or existing_user.instagram,
        "role": role or existing_user.role,
        "profile_picture": existing_user.profile_picture,
        "delivery_cost": delivery_cost or existing_user.delivery_cost,
        "time_prepare": time_prepare or existing_user.time_prepare,

    }

    result = repo.update_user(id, user_data)

    if result:
        print(existing_user.name)
        return JSONResponse(content=jsonable_encoder(existing_user), status_code=200)
    else:
        return JSONResponse(content={'message': 'update user error'}, status_code=500)


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
    repo: UserRepository = UserRepository(sess)
    user = repo.get_user_me(current_user)

    if user:
        # Use the get_addresses method to retrieve user addresses
        addresses = [address for address in user.addresses]
        isworkings = [work for work in user.isworking]

        # Include addresses in the response
        user_data = {
            "id": str(user.id),
            "name": user.name,
            "delivery_cost": user.delivery_cost,
            "time_prepare": user.time_prepare,
            "birthdate": user.birthdate,
            "document": user.document,
            "phone": user.phone,
            "email": user.email,
            "password": user.password,
            "instagram": user.instagram,
            "profile_picture": user.profile_picture,
            "role": user.role,
            "addresses": addresses,
            "isworking": isworkings 
        }

        return user_data
    else:
        return JSONResponse(content={'message': 'User not found'}, status_code=status.HTTP_404_NOT_FOUND)


@router.get('/stories')
def get_users_store(sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_stories()
    return result


@router.get('/establishment')
def get_users_store(sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_establishment()
    return result
