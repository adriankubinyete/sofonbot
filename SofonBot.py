from typing import Optional
import discord
import importlib
import inspect
import os
import time
from aiohttp import ClientSession
from discord import app_commands
from discord.ext import commands

class SofonBot(discord.Client):
    def __init__(
        self,
        *args,
        command_prefix: str = "s!",
        when_mentioned: bool = False,
        web_client: ClientSession,
        intents: Optional[discord.Intents] = None,
        testing_guild_id: Optional[int] = None,
    ):
        """Initialization of the client."""
        if intents is None:
            intents = discord.Intents.default()
        intents.members = True
        
        super().__init__(intents=intents)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.tree = app_commands.CommandTree(self)
        self.command_prefix = command_prefix
        self.prefix_commands = commands.Bot(
            command_prefix=command_prefix if when_mentioned else None,
            intents=intents,
        )  # Usado para adicionar eventos e comandos prefixados.

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
            await self.load_slash_commands()
            await self.load_prefix_commands()
            await self.load_events()

            print("setup_hook: syncing tree...")    
            await self.tree.sync()

        except Exception as e:
            print(f"setup_hook: error loading\n{e}")

    async def load_slash_commands(self) -> None:
        """Load slash commands dynamically."""
        # print('load_slash_command: starting...')
        start_time = time.time()
        commands_folder = os.path.join(os.path.dirname(__file__), "commands")
        
        for filename in os.listdir(commands_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"commands.{filename[:-3]}"  # Remove ".py" extension
                module = importlib.import_module(module_name)

                # Inspeciona todas as funções do módulo
                for name, obj in inspect.getmembers(module):
                    if isinstance(obj, app_commands.Command):
                        self.tree.add_command(obj)
                        # print(f"{module_name} -> {obj.name}")
        elapsed_time = time.time() - start_time
        print(f'load_slash_command: took {elapsed_time:.2f} seconds to load slash commands.')
                        
    async def load_prefix_commands(self) -> None:
        """Placeholder for loading prefix-based commands."""
        # print('load_prefix_commands: starting...')
        start_time = time.time()
        print("load_prefix_commands: Prefix-based commands is not yet implemented.")
        elapsed_time = time.time() - start_time
        print(f'load_prefix_commands: took {elapsed_time:.2f} seconds to load prefix commands.')
        
    async def load_events(self) -> None:
        """Carrega eventos dinamicamente."""
        # print('load_events: starting...')
        start_time = time.time()
        
        events_folder = os.path.join(os.path.dirname(__file__), "events")

        for filename in os.listdir(events_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"events.{filename[:-3]}"  # Remove ".py" extension
                module = importlib.import_module(module_name)

                # Verifica se o módulo possui funções para eventos
                for name, obj in inspect.getmembers(module):
                    if name.startswith("on_") and callable(obj):  # Nome do evento começa com "on_" e é uma função
                        
                        # confere se esse método já não existe na classe SofonBot
                        if hasattr(self, name):
                            # print(f"{module_name} -> {name} (already exists, skipping)")
                            continue
                        
                        # adiciona esse método à classe SofonBot
                        setattr(self, name, obj)
                        # print(f"{module_name} -> {name}")
                        
        elapsed_time = time.time() - start_time
        print(f'load_events: took {elapsed_time:.2f} seconds to load events commands.')
