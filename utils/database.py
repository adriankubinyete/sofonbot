import logging
from pymongo import MongoClient

logger = logging.getLogger("sofonbot.database")

class DatabaseClient:
    _instance = None
    
    def __new__(cls, uri, database):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(uri)
            cls._instance.database = cls._instance.client[database]
        return cls._instance
    
    def get_collection(self, collection_name):
        return self.database[collection_name]
    
    