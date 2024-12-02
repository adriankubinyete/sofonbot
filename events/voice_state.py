import discord
import logging

logger = logging.getLogger("discord")

async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    """Monitora a entrada e saída de usuários no canal de voz."""
    if before.channel:
        print(f'Member {member.name} left voice channel {before.channel}')

    if after.channel:
        print(f'Member {member.name} joined voice channel {after.channel}')
