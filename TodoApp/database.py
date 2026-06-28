# Contains:Database setup and connection configuration Setting up everything needed for FastAPI to talk to database,It:
# creates DB connection manager
# creates session factory
# creates base model class


# Database URL
#       ↓
# Engine created
#       ↓
# Session factory created
#       ↓
# Base model class created


from sqlalchemy import create_engine  # Used to create connection with database.
from sqlalchemy.orm import sessionmaker  # temporary conversation with database

# from sqlalchemy.ext.declarative import declarative_base         #creates base class for SQLAlchemy models.
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:roman@postgres:5432/TodoApplicationDatabase"
#                   #Tell SQLAlchemy which database to use


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# with engine.connect() as conn:
#     print("Connected!")

# Engine = actual database connection manager.How to connect to database,Create database connection manager
# Engine = highway to database


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This creates sessions for database operations.
Base = declarative_base()


# Engine =  knows how to communicate with DB
# sessionmaker:  machine that create session
# session:  Actual conversation with database

# connect_args={'check_same_thread': False}=Allow FastAPI to use SQLite across multiple threads,SQLite has threading restrictions.FastAPI uses multiple requests concurrently.

# bind=engine : Connect sessions to this engine


# Component-------->Responsibility

# URL-------------->where DB exists
# engiNE----------->manages DB connectivity
# sessionmakeR----->creates sessions
# session---------->active DB conversation
# Base------------->parent for models
