from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_DB_URL)
        self.db = self.client[Config.MONGO_DB_NAME]

database = Database()