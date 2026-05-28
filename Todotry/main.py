from fastapi import FastAPI,Depends,HTTPException
from database import engine,SessionLocal
# import models
# from models import Todos,Worker
# models.Base.metadata.create_all(bind=engine)
# from sqlalchemy.orm import Session
from pydantic import BaseModel
from routers import todos,auth
app = FastAPI()
app.include_router(todos.router)
app.include_router(auth.router)



# def get_db():                   #get_db()=opening session,giving session,closing session
#     db = SessionLocal()         #Open a database session
#     try:
#         yield db                #Give this database session to the route function
#     finally:
#         db.close()              #After request finishes,close the database connection

# class TodoRequest(BaseModel):   #validate incoming API request or check incoming data from frontend
#     title: str
#     description: str
#     priority: int
#     complete: bool
#     owner_id: int

# Common                Naming Patterns
# Name	                Purpose
# TodoRequest	        incoming API data
# TodoResponse	        outgoing API response
# TodoCreate	        create schema
# TodoUpdate	        update schema
# Todo	                generic/simple schema
# Todos	                SQLAlchemy DB model

# @app.post("/todos/")
# async def create_todos(
#     req_by_user: TodoRequest,
#     db: Session = Depends(get_db)
# ):

#     todo_model = Todos(**req_by_user.model_dump())

#     db.add(todo_model)
#     db.commit()
#     db.refresh(todo_model)

#     return todo_model


# @app.get("/todos/{todo_id}")
# async def read_by_id(user_id: int, db: Session= Depends(get_db)):
#     filtered=db.query(Todos).filter(Todos.id == user_id).first()
#     return filtered

# @app.get("/todos/")
# async def read(db: Session= Depends(get_db)):
#     return db.query(Todos).all()

# @app.put("/todos/{todo_id}")
# async def update(
#     todo_id: int,
#     req_by_user: TodoRequest,
#     db: Session = Depends(get_db)
# ):

#     todo_model = (
#         db.query(Todos)
#         .filter(Todos.id == todo_id)
#         .first()
#     )

#     if todo_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Todo not found"
#         )

#     todo_model.title = req_by_user.title
#     todo_model.description = req_by_user.description
#     todo_model.priority = req_by_user.priority
#     todo_model.complete = req_by_user.complete
#     todo_model.owner_id = req_by_user.owner_id
    
#     #or update_data = req_by_user.model_dump()

#     # for key, value in update_data.items():
#     #     setattr(todo_model, key, value)

#     db.commit()
#     db.refresh(todo_model)

#     return todo_model

# @app.delete("/todos/")
# async def delete_all_todos(
#     db: Session = Depends(get_db)
# ):

#     db.query(Todos).delete()

#     db.commit()

#     return {"message": "All todos deleted"}

# @app.delete("/todos/{todo_id}")
# async def delete_by_id(
#     todo_id: int,
#     db: Session = Depends(get_db)
# ):

#     todo_model = (
#         db.query(Todos)
#         .filter(Todos.id == todo_id)
#         .first()
#     )

#     if todo_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Todo not found"
#         )

#     db.delete(todo_model)

#     db.commit()

#     return {"message": "Todo deleted successfully"}