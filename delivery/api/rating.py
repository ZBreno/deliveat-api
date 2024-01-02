from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.rating import RatingReq
from repository.sqlalchemy.rating import RatingRepository
from uuid import UUID, uuid4
from datetime import datetime

router = APIRouter(prefix='/rating', tags=['Rating'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_rating(req: RatingReq, sess: Session = Depends(sess_db)):
    repo: RatingRepository = RatingRepository(sess)
    rating = req.model_dump()
    rating['id'] = uuid4()
    rating['created_at'] = datetime.now()
    
    result = repo.insert_rating(rating)
    
    if result:
        return JSONResponse(content=jsonable_encoder(rating), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create rating problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_rating(id: UUID, req: RatingReq, sess: Session = Depends(sess_db)):
    
    rating = req.model_dump(exclude_unset=True)
    repo: RatingRepository = RatingRepository(sess)
    
    result = repo.update_rating(id, rating)
    
    if result:
        return JSONResponse(content=jsonable_encoder(rating), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update rating error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_rating(id: UUID, sess: Session = Depends(sess_db)):
    repo: RatingRepository = RatingRepository(sess)
    result = repo.delete_rating(id)
    
    if result:
        return JSONResponse(content={'message': 'rating deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete rating error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_rating(sess: Session = Depends(sess_db)):
    repo: RatingRepository = RatingRepository(sess)
    result = repo.get_all_rating()
    return result


@router.get("/get/{id}")
def get_rating(id: UUID, sess: Session = Depends(sess_db)):
    repo: RatingRepository = RatingRepository(sess)
    result = repo.get_rating(id)
    return result