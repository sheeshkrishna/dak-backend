from sqlmodel import Session, select
from .models import User, DAK
from .auth import get_password_hash
from fastapi import HTTPException

def create_user(session: Session, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_user(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def create_dak(session: Session, title: str, description: str, created_by: int):
    dak = DAK(title=title, description=description, created_by=created_by)
    session.add(dak)
    session.commit()
    session.refresh(dak)
    return dak

def list_daks(session: Session):
    return session.exec(select(DAK)).all()
