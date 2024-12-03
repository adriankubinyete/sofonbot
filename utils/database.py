from motor.motor_asyncio import AsyncIOMotorClient
import os

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    async def connect(self):
        """Conecta ao MongoDB."""
        if self.client is None:
            uri = os.getenv("DATABASE_URI")
            db_name = os.getenv("DATABASE_NAME")
            if not uri or not db_name:
                raise ValueError("As variáveis DATABASE_URI e DATABASE_NAME precisam estar definidas.")
            
            self.client = AsyncIOMotorClient(uri)
            self.db = self.client[db_name]
            print(f"Conectado ao banco de dados: {db_name}")

    async def disconnect(self):
        """Desconecta do MongoDB."""
        if self.client:
            self.client.close()
            print("Desconectado do banco de dados.")
            self.client = None
            self.db = None

    def get_collection(self, collection_name: str):
        """Retorna uma coleção específica."""
        if not self.db:
            raise ConnectionError("O banco de dados não está conectado.")
        return self.db[collection_name]
