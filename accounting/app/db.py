import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'accounting_db')

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]