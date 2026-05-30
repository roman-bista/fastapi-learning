from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users  
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
bcrypt_context= CryptContext(schemes=['bcrypt'], deprecated='auto')
class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str



def get_db():                   #get_db()=opening session,giving session,closing session
    db = SessionLocal()         #Open a database session
    try:
        yield db                #Give this database session to the route function
    finally:
        db.close()              #After request finishes,close the database connection

# Create database connection            
# ↓
# Give it to API temporarily
# ↓
# After work is done
# ↓
# Close connection safely

# Open table
# ↓
# Customer uses table
# ↓
# Customer leaves
# ↓
# Clean and close table


# Session = conversation with database,Using a session, your app can:

# read data
# add data
# update data
# delete data
# save changes
       
db_dependency = Annotated[Session, Depends(get_db)]     #FastAPI:
                                                        # Run get_db()
                                                        # ↓
                                                        # Get database session
                                                        # ↓
                                                        # Inject it into db variable
def authenticate_user(username: str, password: str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model=Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name= create_user_request.first_name,
        last_name=create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    return {
        "message": "User created successfully",
        "user_id": create_user_model.id
    }

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db : db_dependency):
    user=authenticate_user(form_data.username,form_data.password, db)
    if not user:
        return 'failed authentication'
    return 'sucessful authentication' 