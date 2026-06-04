from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status,Path #Import models so SQLAlchemy knows which tables exist
from models import Todos,Users
from database import SessionLocal   #Import database connection engine and session factory    
from .auth import get_current_user
from passlib.context import CryptContext
 
router = APIRouter(
    prefix='/user',
    tags=['user'])        


def get_db():                   #get_db()=opening session,giving session,closing session
    db = SessionLocal()         #Open a database session
    try:
        yield db                #Give this database session to the route function
    finally:
        db.close() 

db_dependency = Annotated[Session, Depends(get_db)] 
user_dependency= Annotated[dict,Depends(get_current_user)] #which tells us who is making the request.
bcrypt_context= CryptContext(schemes=['bcrypt'], deprecated='auto')

class Userverification(BaseModel):
    password: str
    new_password: str=Field(min_length=6)

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='authentication failed')
    return db.query(Users).filter(Users.id==user.get('user_id')).first()

@router.put('/password',status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency,db: db_dependency, user_verification: Userverification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model=db.query(Users).filter(Users.id== user.get('user_id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail=" error on password change")
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
@router.put("/phonenumber/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    user_model= db.query(Users).filter(Users.id == user.get('user_id')).first()
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()