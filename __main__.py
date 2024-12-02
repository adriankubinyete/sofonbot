import asyncio
import logging
import logging.handlers
import os
from aiohttp import ClientSession
from dotenv import load_dotenv
from typing import List, Optional

from SofonBot import SofonBot

async def main():
    """main func"""
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    
    handler = logging.handlers.RotatingFileHandler(
        filename=f"{os.getenv('DATABASE_VOLUME')}/discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  #32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", date_format, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # start async session
    async with ClientSession() as web_client:
        async with SofonBot(
            # commands.when_mentioned,
            command_prefix="s!",
            when_mentioned=True,
            web_client=web_client,
            testing_guild_id=os.getenv("TESTING_GUILD_ID", None),
        ) as client:
            await client.start(os.getenv("DISCORD_TOKEN", ""))
            
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())