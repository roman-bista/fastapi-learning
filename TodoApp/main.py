# Starts FastAPI app and tells SQLAlchemy:“Create tables in database.” define routes

from typing import Annotated
from routers import auth, todos, admin, users
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status,Path #Import models so SQLAlchemy knows which tables exist
from models import Todos
from database import engine, SessionLocal   #Import database connection engine and session factory
import models    

app=FastAPI()          

models.Base.metadata.create_all(bind=engine)        #Take all SQLAlchemy models
                                                    # ↓
                                                    # Convert Python classes into SQL tables
                                                    # ↓
                                                    #Create tables in database if they do not already exist

# engine = object that knows how to connect to database Engine = connection manager
# Session = active conversation
# SessionLocal=Creates database sessions

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# def get_db():                   #get_db()=opening session,giving session,closing session
#     db = SessionLocal()         #Open a database session
#     try:
#         yield db                #Give this database session to the route function
#     finally:
#         db.close()              #After request finishes,close the database connection

# # Create database connection            
# # ↓
# # Give it to API temporarily
# # ↓
# # After work is done
# # ↓
# # Close connection safely

# # Open table
# # ↓
# # Customer uses table
# # ↓
# # Customer leaves
# # ↓
# # Clean and close table


# # Session = conversation with database,Using a session, your app can:

# # read data
# # add data
# # update data
# # delete data
# # save changes
       
# db_dependency = Annotated[Session, Depends(get_db)]     #FastAPI:
#                                                         # Run get_db()
#                                                         # ↓
#                                                         # Get database session
#                                                         # ↓
#                                                         # Inject it into db variable


# class TodoRequest(BaseModel):       #BaseModel :automatically provides validation
#                                      #TodoRequest:Validation model for incoming todo requests
#     title: str = Field(min_length=3)
#     description: str= Field(min_length=10, max_length=100)
#     priority: int= Field(gt=0,lt=6)
#     complete: bool



# @app.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db: db_dependency, ):
#     return db.query(Todos).all()                         #SELECT * FROM todos;

# @app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)     #return http 200 on sucess
# async def read_todo(db: db_dependency, todo_id: int=Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

#     if todo_model is not None:              #means there is some data inside todo model
#         return todo_model 
    
#     raise HTTPException(status_code=404, detail="todo does not exist")  #If todo not found,return HTTperroresponse

# @app.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(db: db_dependency, todo_request: TodoRequest):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()


# @app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db: db_dependency, 
#                       todo_request: TodoRequest,
#                       todo_id: int=Path(gt=0), 
#                       ):
#     todo_model= db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail=" Todo not found.")
    
#     todo_model.title= todo_request.title #Replace old title with new title from request body
#     todo_model.description= todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete
#     db.add(todo_model)
#     db.commit()

# @app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model= db.query(Todos).filter(Todos.id== todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()