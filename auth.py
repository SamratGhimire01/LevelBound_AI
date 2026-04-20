from fastapi import APIRouter
from gunicorn import app
from database import collection
from models import users,login
from schema import serial_user_helper,user_helper
from bson import ObjectId
auth_router = APIRouter()
@auth_router.get('/')
async def get_all():
    results = serial_user_helper(await collection.find().to_list(100))
    return {"status":"ok","Data": results}

@auth_router.post('/register')
async def register(user:users):
    new_user = await collection.insert_one(dict(user))
    user = user_helper(await collection.find_one({"_id":new_user.inserted_id}))
    return {"status":"ok","User_added": user}

@auth_router.post('/login')
async def login(info:login):
    query = {
        "username": info.username, 
        "hashed_password": info.hashed_password
    }
    user_data = await collection.find_one(query)
    if not user_data:
        return {"Error" : "Invalid Creditial"}
    data = user_helper(user_data)
    return {"Greeting's": f"Hello {data['username']}. Ready to Start the journey."}