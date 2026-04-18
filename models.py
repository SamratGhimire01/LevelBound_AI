from pydantic import BaseModel

class users(BaseModel):
    username: str
    hashed_password : str
    level : int
    exp : int
    streak : int