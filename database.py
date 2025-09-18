from sqlmodel import SQLModel, create_engine, Session
import os

# Import all your models here to make sure SQLModel's metadata knows about them
from models import Attachments, AuditLogs, DakDocuments, Departments, Escalations, MovementLogs, Notifications, Users
from sqlmodel import SQLModel, create_engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine, tables=[
        Users.__table__,
        Departments.__table__,
        DakDocuments.__table__,
        Attachments.__table__,
        AuditLogs.__table__,
        Escalations.__table__,
        MovementLogs.__table__,
        Notifications.__table__,
    ])


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    # Import each model individually if necessary to register tables explicitly
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

