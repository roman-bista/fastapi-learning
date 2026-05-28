from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel, Field,EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Worker
from database import get_db

router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str=Field(gt= 3)
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
async def authorize(req: CreateUserRequest, db: Session = Depends(get_db)):
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