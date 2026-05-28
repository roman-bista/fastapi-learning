from sqlalchemy import create_engine                            #Used to create connection with database.
from sqlalchemy.orm import sessionmaker                         #temporary conversation with database
from sqlalchemy.ext.declarative import declarative_base         #creates base class for SQLAlchemy models.

SQLALCHEMY_DATABASE_URL='sqlite:///./todosrouter.db'                   #Tell SQLAlchemy which database to use
engine= create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) #This connects FastAPI ↔ SQLite database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)   #This creates database sessions/connections.
Base=declarative_base()   
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()