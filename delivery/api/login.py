from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from fastapi.security import OAuth2PasswordBearer
from domain.request.user import LoginReq
from domain.data.sqlalchemy_models import User
from jose import JWTError, jwt
from uuid import uuid4
from domain.request.user import UserReq
from repository.sqlalchemy.user import UserRepository
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix='/auth', tags=['Auth'])

SECRET_KEY = "klhfdsafdf16544236541623522dfsdfsd"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except JWTError:
        raise credentials_exception

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

@router.post("/token", response_model=dict)
async def login_for_access_token(user: LoginReq, sess: Session = Depends(sess_db)):
    db_user = sess.query(User).filter(User.email == user.email).first()
    if db_user and user.password == db_user.password:
        token_data = {"sub": user.email}
        token = create_jwt_token(token_data)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
def add_user(req: UserReq, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    user = req.model_dump()
    user['id'] = uuid4()
    
    result = repo.insert_user(user)
    
    if result:
        return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create user problem encountered'}, status_code=status.HTTP_400_BAD_REQUEST)