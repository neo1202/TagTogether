from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.user_model import User
from dotenv import load_dotenv
import os

load_dotenv()

# Retrieve the database URLs from environment variables
DATABASE_URL_WRITER = os.getenv("DATABASE_URL_WRITER")
DATABASE_URL_READER = os.getenv("DATABASE_URL_READER")

# Create database engines
engine_writer = create_engine(DATABASE_URL_WRITER, echo=True)
engine_reader = create_engine(DATABASE_URL_READER, echo=True)

# Create session factories
SessionLocalWriter = sessionmaker(autocommit=False, autoflush=False, bind=engine_writer)
SessionLocalReader = sessionmaker(autocommit=False, autoflush=False, bind=engine_reader)

# Dependency: Get a database session for writing
def get_db_writer():
    db = SessionLocalWriter()
    try:
        yield db
    finally:
        db.close()

# Dependency: Get a database session for reading
def get_db_reader():
    db = SessionLocalReader()
    try:
        yield db
    finally:
        db.close()

# Database operation function
def get_user(db: Session, user_name: str) -> User:
    return db.query(User).filter(User.user_name == user_name).first()

from app.models.base import Base
Base.metadata.create_all(bind=engine_writer)  # Create all tables using the writer engine