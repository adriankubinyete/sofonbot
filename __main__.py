import asyncio
import logging
import logging.handlers
import os
import colorlog
from aiohttp import ClientSession
from dotenv import load_dotenv
from typing import List, Optional
from utils.database import Database

from SofonBot import SofonBot

async def main():
    """main func"""
    
    # preparing logger
    discord_logger = logging.getLogger("discord")
    sofon_logger = logging.getLogger("sofonbot")
    
    # setting level
    discord_logger.setLevel(logging.INFO)
    sofon_logger.setLevel(logging.DEBUG)
    
    # creating the handlers
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f"{os.getenv('LOG_VOLUME')}/everything.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  #32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    console_handler = logging.StreamHandler()
    
    # setting format for each handler
    date_format = "%Y-%m-%d %H:%M:%S"
    file_formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", date_format, style="{")
    file_handler.setFormatter(file_formatter)
    
    color_formatter = colorlog.ColoredFormatter(
        fmt="[%(asctime)s] [%(log_color)s%(levelname)-8s%(reset)s] %(log_color)s%(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        reset=True,
    )
    console_handler.setFormatter(color_formatter)
    
    # registering file handler
    discord_logger.addHandler(file_handler)
    sofon_logger.addHandler(file_handler)
    
    # registering console handler
    discord_logger.addHandler(console_handler)
    sofon_logger.addHandler(console_handler)
    
    # start async session
    async with ClientSession() as web_client:
        async with Database(
            uri=os.getenv("DATABASE_URI"), 
            database=os.getenv("DATABASE_NAME")
        ) as mongodb_client:
            async with SofonBot(
                command_prefix=os.getenv("BOT_PREFIX", "s!"),
                when_mentioned=True,
                web_client=web_client,
                testing_guild_id=os.getenv("BOT_TESTING_GUILD_ID", None),
                database=mongodb_client
            ) as client:
                await client.start(os.getenv("BOT_TOKEN", ""))
            
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())