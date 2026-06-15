# Starts FastAPI app and tells SQLAlchemy:“Create tables in database.” define routes

from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status,Path #Import models so SQLAlchemy knows which tables exist
from ..models import Todos
from ..database import SessionLocal   #Import database connection engine and session factory    
from .auth import get_current_user
router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)         



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
       
db_dependency = Annotated[Session, Depends(get_db)] 
                                                       # Run get_db()
                                                        # ↓
                                                        # Get database session
                                                        # ↓
                                                        # Inject it into db variable

#FastAPI dependency injection provides a SQLAlchemy Session object through get_db().
#The Session is used to communicate with the database and perform CRUD operations using ORM queries.
#think like atm card:Deposit money,Withdraw money,Check balance

user_dependency= Annotated[dict,Depends(get_current_user)] #which tells us who is making the request.
class TodoRequest(BaseModel):           #BaseModel :automatically provides validation
                                        #TodoRequest:Validation model for incoming todo requests
    title: str = Field(min_length=3)
    description: str= Field(min_length=10, max_length=100)
    priority: int= Field(gt=0,lt=6)
    complete: bool



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: db_dependency, ):
    if user is None:
        raise HTTPException(status_code=401,detail="authetication failed")
    return db.query(Todos).filter(Todos.owner_id==user.get('user_id')).all()                        #SELECT * FROM todos;

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)     #return http 200 on sucess
async def read_todo(user:user_dependency,db: db_dependency, todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="authetication failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()

    if todo_model is not None:              #means there is some data inside todo model
        return todo_model 
    
    raise HTTPException(status_code=404, detail="todo does not exist")  #If todo not found,return HTTperroresponse

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="authetication failed")
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()
    
@router.put("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int=Path(gt=0), 
                      ):
    if user is None:
        raise HTTPException(status_code=401,detail="authetication failed")
    
    todo_model= db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("user_id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail=" Todo not found.")
    
    todo_model.title= todo_request.title #Replace old title with new title from request body
    todo_model.description= todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="authetication failed")
    todo_model= db.query(Todos).filter(Todos.id== todo_id).filter(Todos.owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).delete()
    db.commit()