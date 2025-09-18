from sqlmodel import SQLModel, create_engine, Session
import os

# Import all your models here to make sure SQLModel's metadata knows about them
import models  # this imports all the models in your models.py

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    # Import each model individually if necessary to register tables explicitly
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
