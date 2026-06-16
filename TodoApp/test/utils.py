from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from TodoApp.main import app
import pytest
from ..models import Todos
from ..routers.todos import get_current_user,get_db


def override_get_current_user():
    return {'username': 'codingwithroman',
            'user_id':1,
            'user_role':'admin'}

def override_get_db():        # Override FastAPI's get_db dependency
                              # so tests use SQLite instead of PostgreSQL.
    db = TestingSessionLocal()                  
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

SQLALCHEMY_DATABASE_URL= "sqlite:///./testdb.db"                    #Create a Test Database

engine= create_engine(SQLALCHEMY_DATABASE_URL,                      #Creates a connection to:testdb.db
                      connect_args={"check_same_thread": False},
                      poolclass= StaticPool) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)           #3. Create Testing Session
Base.metadata.create_all(bind=engine)                                           #Creates all tables in the test database.


def override_get_current_user():
    return {'username': 'codingwithroman',
            'user_id':1,
            'user_role':'admin'} 

client=TestClient(app)


@pytest.fixture
def test_todo():
    todo=Todos(
        title='learn to code',
        description="need to learn everyday",
        priority=5,
        complete= False,
        owner_id=1
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo

    db.query(Todos).delete()
    db.commit()
    db.close()