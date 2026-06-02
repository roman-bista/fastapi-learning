from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel, Field,EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Worker
from database import get_db
from fastapi.security import OAuth2PasswordBearer

from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone

from dotenv import load_dotenv
import os

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") #Authorization: Bearer abc123xyz
                                                                #         ↓
                                                                # remove "Bearer "
                                                                #         ↓
                                                                # abc123xyz

                                                                #and then passes to function



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)
def create_access_token(username: str, user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
    "sub": username,
    "id": user_id,
    "exp": expires
}
    token= jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: str

bcrypt_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)
@router.post("/auth/")
async def create_user(req: CreateUserRequest, db: Session = Depends(get_db)):
    encrypted_pw = bcrypt_context.hash(req.password)    
    user_model = Worker(
    username=req.username,
    email=req.email,
    first_name=req.first_name,
    last_name=req.last_name,
    hashed_password=encrypted_pw,
    role=req.role,
    is_active=True
)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/token")
async def login(req: LoginRequest,db: Session = Depends(get_db)):

    user = db.query(Worker).filter(Worker.username == req.username).first()
    if user is None:
        raise HTTPException( status_code=401, detail="Invalid username or password" )
    
    password_matches = bcrypt_context.verify( req.password, user.hashed_password )

    if not password_matches: 
        raise HTTPException( status_code=401, detail="Invalid username or password" )
    
    access_token = create_access_token(user.username,user.id) 

    return {
    "access_token": access_token,
    "token_type": "bearer"
}

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
        return {
            "username": username,
            "user_id": user_id}
    
    except JWTError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user")


# @router.post("/token")
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db : db_dependency):
#     user=authenticate_user(form_data.username,form_data.password, db)
#     if not user:
#         return 'failed authentication'
#     return 'sucessful authentication'
# User Login
#     ↓
# Username + Password
#     ↓
# Verify password
#     ↓
# create_access_token()
#     ↓
# JWT Token
#     ↓
# Client stores token
# ------------------------------------------------
# GET /todos
# Authorization: Bearer eyJhbGc...
#     ↓
# OAuth2PasswordBearer
#     ↓
# token = "eyJhbGc..."
#     ↓
# get_current_user()
#     ↓
# jwt.decode()
#     ↓
# payload
#     ↓
# sub + id
#     ↓
# current_user
#     ↓
# /todos route