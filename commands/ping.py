import logging
import discord
from discord.ext import commands
from discord import app_commands
from utils.methods import methods

logger = logging.getLogger("sofonbot.command.ping")

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        
    @app_commands.command(name="ping", description="Pong")
    async def ping(self, interaction: discord.Interaction):
        logger.info("Ping command called")
        await interaction.response.send_message("Pong!")

async def setup(bot):
    await bot.add_cog(PingCommand(bot))