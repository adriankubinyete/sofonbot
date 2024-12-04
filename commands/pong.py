import logging
import discord
from discord.ext import commands
from discord import app_commands
from utils.methods import methods

logger =  logging.getLogger("sofonbot.command.pong")

class PongCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        
    @app_commands.command(name="pong", description="Ping")
    async def pong(self, interaction: discord.Interaction):
        logger.info("Pong command called")
        await interaction.response.send_message("Ping!")

async def setup(bot):
    await bot.add_cog(PongCommand(bot))