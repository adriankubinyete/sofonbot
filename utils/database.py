import logging
import os
from pymongo import MongoClient

logger = logging.getLogger("sofonbot.database")

class DatabaseClient:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(os.getenv("DATABASE_URI"))
            cls._instance.database = cls._instance.client[os.getenv("DATABASE_NAME")]
        return cls._instance

    def __aenter__(self):
        # No caso de operações assíncronas, o cliente poderia realizar algo aqui
        # Aqui, você pode retornar a instância do cliente se precisar de algo específico
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        # Limpeza ou fechamento da conexão, caso necessário
        self.client.close()
    
    def get_collection(self, collection_name):
        return self.database[collection_name]
    
    