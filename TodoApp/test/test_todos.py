from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from TodoApp.main import app
from TodoApp.routers.todos import get_db
from ..routers.auth import get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL= "sqlite:///./testdb.db"                    #Create a Test Database

engine= create_engine(SQLALCHEMY_DATABASE_URL,                      #Creates a connection to:testdb.db
                      connect_args={"check_same_thread": False},
                      poolclass= StaticPool) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)           #3. Create Testing Session
Base.metadata.create_all(bind=engine)                                           #Creates all tables in the test database.

def override_get_db():        # Override FastAPI's get_db dependency
                              # so tests use SQLite instead of PostgreSQL.
    db = TestingSessionLocal()                  
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'codingwithroman',
            'user_id':1,
            'user_role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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
    # with engine.connect() as connection:
    #     connection.execute(text("DELETE FROM todos;"))
    #     connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/todos") 
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False,
                                'title':'learn to code',
                                'description':'need to learn everyday',
                                'id': 1,
                                'priority': 5,
                                'owner_id':1}]

    
def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1") 
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False,
                                'title':'learn to code',
                                'description':'need to learn everyday',
                                'id': 1,
                                'priority': 5,
                                'owner_id':1}
    
def test_read_one_authenticated_not_found():
    response=client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "todo does not exist"}

def test_create_todo():
    request_data={
        'title':'New Todo',
        'description':'New todo description',
        # 'id': 1,
        'priority': 5,
        'complete':False
    }
    response=client.post("/todos/",json = request_data)

    assert response.status_code == 201

    db=TestingSessionLocal()
    todo = db.query(Todos).filter(
        Todos.title == "New Todo"
    ).first()

    assert todo is not None
    assert todo.title == "New Todo"
    assert todo.description == "New todo description"
    assert todo.priority == 5
    assert todo.complete is False

def test_update_todo(test_todo):
    request_data = {
        "title": "changed",
        "description": "need to learn everyday",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/1", json=request_data)

    assert response.status_code == 204

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == "changed"

    
def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "changed",
        "description": "need to learn everyday",
        "priority": 5,
        "complete": False
    }

    response = client.put("/todos/999", json=request_data)

    assert response.status_code == 404
    assert response.json()=={'detail' : 'Todo not found.'}

def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == 204
    db =TestingSessionLocal()
    Model=db.query(Todos).filter(Todos.id==1).first()
    assert Model is None
def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()=={'detail':'Not Found'}