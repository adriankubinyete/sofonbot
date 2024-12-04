import discord
import os
import logging
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("sofonbot.checks")

def is_me():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == os.getenv("BOT_OWNER") or interaction.user.id in os.getenv("BOT_OWNER")
    return app_commands.check(predicate)
    
def is_test_guild():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild.id == os.getenv("TESTING_GUILD_ID" or interaction.guild.id in os.getenv("TESTING_GUILD_ID"))
    return app_commands.check(predicate)
    
def funny():
    def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id in [1083013666074546277]:
            logger.debug(f"baiter detectado!")
            # interaction.user.name = "Baiter"
        elif interaction.user.id in [1087873539635433522]:
            logger.debug(f"cone detectado!")
            # interaction.user.name = "Cone"
        return True
    return app_commands.check(predicate)