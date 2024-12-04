import discord
from discord.ext import commands
import logging

# Configuração do logger
logger = logging.getLogger("sofonbot.event.voice_state")

class VoiceStateMonitor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()  # Decorador que registra o evento de mudança de estado de voz
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """Monitora a entrada e saída de usuários no canal de voz."""
        if before.channel:
            print(f'Member {member.name} left voice channel {before.channel}')
        
        if after.channel:
            print(f'Member {member.name} joined voice channel {after.channel}')

# Função para carregar a cog no bot
async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceStateMonitor(bot))
