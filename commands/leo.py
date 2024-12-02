import logging

import discord
from discord import app_commands

from random import randint

logger = logging.getLogger("discord")

@app_commands.command(name="leo", description="o que o leonardo é")
async def leo(
    interaction: discord.Interaction,
) -> None:
    """Troll"""
    
    if randint(1, 100) == 1:
        await interaction.response.send_message("god")
    else:
        await interaction.response.send_message("baiter")