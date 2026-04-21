from pydantic import BaseModel , EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str
    level : int = 1
    exp : int = 0
    streak : int = 0

class UserLogin(BaseModel):
    username : str
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"
    
class Token_Data(BaseModel):
    username : Optional[str] = None