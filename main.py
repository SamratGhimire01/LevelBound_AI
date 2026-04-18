from fastapi import FastAPI
from database import collection
from models import users
from schema import serial_user_helper,user_helper
from bson import ObjectId
app = FastAPI()

@app.get('/')
async def get_all():
    results = serial_user_helper(await collection.find().to_list(100))
    return {"status":"ok","Data": results}

@app.post('/register')
async def register(user:users):
    new_user = await collection.insert_one(dict(user))
    user = user_helper(await collection.find_one({"_id":new_user.inserted_id}))
    return {"status":"ok","User_added": user}