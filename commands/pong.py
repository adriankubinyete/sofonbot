import logging

import discord
from discord import app_commands

logger = logging.getLogger("discord")

@app_commands.command(name="pong", description="ping")
async def pong(
    interaction: discord.Interaction,
) -> None:
    """Pong command"""
    await interaction.response.send_message("Ping!", ephemeral=True)

