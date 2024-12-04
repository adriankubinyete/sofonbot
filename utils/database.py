from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger("database")

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri: str = None, database: str = None):
        # Inicializar apenas na primeira vez
        if not hasattr(self, "_initialized"):
            self.client = None
            self.db = None
            self.uri = uri
            self.database_name = database
            self._initialized = True

    async def connect(self):
        """Conecta ao MongoDB."""
        if self.client is None:
            if not self.uri or not self.database_name:
                raise ValueError("URI e nome do banco de dados devem ser fornecidos.")
            
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.database_name]
            logger.info(f"Conectado ao banco de dados: {self.database_name}")

    async def disconnect(self):
        """Desconecta do MongoDB."""
        if self.client:
            self.client.close()
            logger.info("Desconectado do banco de dados.")
            self.client = None
            self.db = None

    def get_collection(self, collection_name: str):
        """Retorna uma coleção específica."""
        if not self.db:
            raise ConnectionError("O banco de dados não está conectado.")
        return self.db[collection_name]

    async def __aenter__(self):
        """Suporte ao uso de async with."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Garante a desconexão ao sair do contexto."""
        await self.disconnect()
