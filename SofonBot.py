from typing import Optional
import discord
import os
import time
import logging
from aiohttp import ClientSession
from discord import app_commands
from discord.ext import commands
from utils.database import Database

logger = logging.getLogger("discord.sofonbot")

class SofonBot(commands.Bot):  # Mudamos para herdar de commands.Bot
    def __init__(
        self,
        *args,
        command_prefix: str = "s!",
        when_mentioned: bool = False,
        web_client: ClientSession,
        intents: Optional[discord.Intents] = None,
        testing_guild_id: Optional[int] = None,
        db: Database = None,
    ):
        """Initialization of the client."""
        if intents is None:
            intents = discord.Intents.default()
        intents.members = True
        
        super().__init__(command_prefix=command_prefix if when_mentioned else None, intents=intents)  # Usamos commands.Bot
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.db = db  # Adicionando o banco de dados à instância

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Logged in as {self.user}")

    async def on_guild_join(self, guild: discord.Guild):
        print(f"Joined {guild.name}")

    async def on_guild_remove(self, guild: discord.Guild):
        print(f"Left {guild.name}")
        
    async def setup_hook(self) -> None:
        """Setup hook for loading commands and events."""
        print("setup_hook: initializing configuration...")
        
        try:
            # Register cogs
            await self.load_cogs()
            
            # Sync tree after loading cogs
            start_time = time.time()
            await self.tree.sync()  # `self.tree` já existe
            elapsed_time = time.time() - start_time
            logger.info(f'Tree took {elapsed_time:.2f} seconds to sync.')
            
        except Exception as e:
            logger.exception(f"setup_hook: error loading\n{e}")

    async def load_cogs(self) -> None:
        cog_dirs = ["commands", "events"]
        cogloader_start_time = time.time()
        
        for directory in cog_dirs:
            for filename in os.listdir(directory):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = f"{directory}.{filename[:-3]}"
                    try:
                        print('Loading cog:', module_name)
                        await self.load_extension(module_name)  # Usamos load_extension diretamente
                        logger.info(f"Loaded cog: {module_name}")
                    except Exception as e:
                        logger.exception(f"load_cogs: error loading {module_name}\n{e}")

        cogloader_elapsed_time = time.time() - cogloader_start_time
        logger.info(f"Cogs took {cogloader_elapsed_time:.2f} seconds to load.")
