from fastapi import APIRouter,HTTPException,Depends,status,Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database import collection
from auth.models import UserCreate, UserLogin, Token, Token_Data
from auth.utils import (verify_password, get_password_hash, create_access_token, decode_token)
from schema import login_user_helper

from datetime import timedelta
from bson import ObjectId


auth_router = APIRouter(tags=["Authentication"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_user_from_db(username:str):
    return await collection.find_one({"username": username})

async def get_current_user(response:Response,token:str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get('sub')
    if username is None:
        raise credentials_exception
    
    user = await get_user_from_db(username)
    if user is None:
        raise credentials_exception
    
    # Sliding Session
    
    new_token = create_access_token(data={'sub':username},expires_delta=timedelta(minutes=30))
    
    # attaching to response header
    
    response.headers["X-New-Token"] = new_token
    
    
    
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user.get("email"),
        "level": user.get("level", 1),
        "exp": user.get("exp", 0),
        "streak": user.get("streak", 0)
    }
    
    

# Register(sign Up)

@auth_router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate):
    existing_user = await get_user_from_db(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username Already Exists")
    
    if user.email:
        existing_email = await collection.find_one({"email":user.email})
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email Already Exists")
    user_data = {
        "username" : user.username,
        "email" : user.email,
        "hashed_password" : get_password_hash(user.password),
        "level" : user.level,
        "exp" : user.exp,
        "streak" : user.streak
        }
    
    result = await collection.insert_one(user_data)
    
    created_user = await collection.find_one({"_id":result.inserted_id})
    
    return login_user_helper(created_user)

# Login(sign in)
@auth_router.post("/login",response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Username or Password",headers={"WWW-Authenticate":"Bearer"})
    
    user = await get_user_from_db(form_data.username)
    if not user:
        raise credentials_exception
    
    if not verify_password(form_data.password,user['hashed_password']):
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token({"sub":user['username']},expires_delta =access_token_expires)
    
    return {"access_token": access_token,"token_type": "bearer"}

@auth_router.get("/me")
async def read_user_me(current_user=Depends(get_current_user)):
    return current_user

# Logout(sign out) - Client side can simply delete the token, but we can also implement token blacklisting for enhanced security.