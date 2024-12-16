import discord
from discord.ext import commands
import logging

# Configuração do logger
logger = logging.getLogger("sofonbot.event.voice_state")

class VoiceStateMonitor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.temporary_channels = set()  # Armazena IDs dos canais temporários

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """Monitora a entrada e saída de usuários no canal de voz."""
        target_channel_id = 1242440826244698192  # Substitua pelo ID do canal que deve ser monitorado

        # Quando o membro entra em um canal
        if after.channel and after.channel.id == target_channel_id:
            guild = member.guild
            category = after.channel.category  # Mantém a categoria do canal original

            # Verifica se o bot tem permissão para criar canais
            bot_member = guild.me
            if not bot_member.guild_permissions.manage_channels:
                logger.error("Permissão insuficiente para criar canais")
                return

            # Usa o apelido do membro na guilda ou o nome padrão
            member_display_name = member.display_name

            # EASTER EGG : Muda a sala baseado no display do user (case insensitive)
            if "rafael" in member_display_name.lower():
                channel_name = f"☂ {member_display_name}'s room"
            elif "adrian" in member_display_name.lower():
                channel_name = f"💫 {member_display_name}'s room"
            elif "andr" in member_display_name.lower():
                channel_name = f"🎀 𝓈𝒶𝓁𝒶 𝒹𝓊 𝒶𝓃𝒹𝓇𝑒𝑒𝒽 🎀"
            elif "leonardo" in member_display_name.lower():
                channel_name = f"🎸 {member_display_name}'s room"
            else:
                channel_name = f"{member_display_name}'s room"

            # Cria um novo canal de voz com o nome do membro
            new_channel = await guild.create_voice_channel(
                name=channel_name,
                category=category
            )
            self.temporary_channels.add(new_channel.id)  # Armazena o ID do canal temporário
            logger.info(f"Criado novo canal: {new_channel.name} para {member_display_name}")
            
            # Move o membro para o novo canal
            await member.move_to(new_channel)

        # Quando o membro sai de um canal
        if before.channel and len(before.channel.members) == 0:
            # Verifica se o bot tem permissão para excluir canais
            bot_member = before.channel.guild.me
            if not bot_member.guild_permissions.manage_channels:
                logger.error("Permissão insuficiente para deletar canais")
                return

            # Exclui o canal apenas se ele for temporário
            if before.channel.id in self.temporary_channels:
                await before.channel.delete()
                self.temporary_channels.remove(before.channel.id)  # Remove da lista de temporários
                logger.info(f"Canal temporário deletado: {before.channel.name}")

# Função para carregar a cog no bot
async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceStateMonitor(bot))