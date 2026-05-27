from fastapi import FastAPI,Depends
from database import engine,SessionLocal
import models
models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

def get_db():                   #get_db()=opening session,giving session,closing session
    db = SessionLocal()         #Open a database session
    try:
        yield db                #Give this database session to the route function
    finally:
        db.close()              #After request finishes,close the database connection

class TodoRequest(BaseModel):   #validate incoming API request or check incoming data from frontend
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int

# Common                Naming Patterns
# Name	                Purpose
# TodoRequest	        incoming API data
# TodoResponse	        outgoing API response
# TodoCreate	        create schema
# TodoUpdate	        update schema
# Todo	                generic/simple schema
# Todos	                SQLAlchemy DB model