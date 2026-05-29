from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel, Field,EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Worker
from database import get_db

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

    user= db.query(Worker).filter(LoginRequest.username == req.username).first()

    if user is None:
        raise HTTPException( status_code=401, detail="Invalid username or password" )
    
    password_matches = bcrypt_context.verify( req.password, user.hashed_password )

    if not password_matches: 
        raise HTTPException( status_code=401, detail="Invalid username or password" ) 
    return { "message": "Login successful" }

# @router.post("/token")
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db : db_dependency):
#     user=authenticate_user(form_data.username,form_data.password, db)
#     if not user:
#         return 'failed authentication'
#     return 'sucessful authentication' 