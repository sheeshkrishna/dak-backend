from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class DAKCreate(BaseModel):
    title: str
    description: str

class DAKRead(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_by: int
