import logging

import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger("discord")

@app_commands.command(name="ping", description="pong")
@commands.is_owner()
async def ping(
    interaction: discord.Interaction,
) -> None:
    """Ping command"""
    await interaction.response.send_message("Pong!", ephemeral=True)
    