from dotenv import load_dotenv,dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
import os

load_dotenv()

Mongo_db = os.getenv("mongodb_url")
client = AsyncIOMotorClient(Mongo_db)
database = client['levelbound']
collection = database['Users']
