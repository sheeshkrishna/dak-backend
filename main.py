from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List

import models
import database
import crud
import auth
import schemas

app = FastAPI()

#database.create_db_and_tables()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(database.get_session)):
    user = crud.get_user(session, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, session: Session = Depends(database.get_session)):
    return crud.create_user(session, user.username, user.password, auth.get_password_hash)

@app.get("/users/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/daks/", response_model=schemas.DAKRead)
def create_dak(dak: schemas.DAKCreate, session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_dak(session, dak.title, dak.description, current_user.id)

@app.get("/daks/", response_model=List[schemas.DAKRead])
def read_daks(session: Session = Depends(database.get_session)):
    return crud.list_daks(session)

