import discord
from discord import app_commands
from discord.ext import commands
from utils.database import DatabaseClient

# class TempChannelMonitor(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot

#     @commands.Cog.listener()  # Decorador que registra o evento de mudança de estado de voz
#     async def on_voice_state_update(
#         self,
#         member: discord.Member,
#         before: discord.VoiceState,
#         after: discord.VoiceState,
#     ) -> None:
#         """Monitora a entrada e saída de usuários no canal de voz."""
#         if before.channel:
#             print(f'Member {member.name} left voice channel {before.channel}')
        
#         if after.channel:
#             print(f'Member {member.name} joined voice channel {after.channel}')

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = DatabaseClient().get_collection('jointocreate')
        
        self.load_existing_channels()

    def load_existing_channels(self):
        """Consulta os canais já configurados no banco de dados."""
        existing_channels = self.db.find({})  # Ou adicione um filtro se necessário

        for channel_data in existing_channels:
            channel_id = channel_data.get('JTC_CHANNEL_ID')
            guild_id = channel_data.get('GUILD_ID')

            # Busca o canal no servidor (guild)
            guild = self.bot.get_guild(guild_id)
            if guild:
                channel = guild.get_channel(channel_id)
                if channel:
                    # Aqui você pode adicionar a lógica de monitoramento do canal ou outras ações
                    print(f"Canal de voz {channel.name} já configurado como JTC no servidor {guild.name}")
                    # Você pode adicionar a lógica para adicionar ouvintes de eventos ou outras interações
                else:
                    print(f"Canal de voz {channel_id} não encontrado no servidor {guild.name}.")
            else:
                print(f"Servidor {guild_id} não encontrado para o canal {channel_id}.")

    # sets up a channel that, once joined, will create tempchannels for each user that joins
    # make a way to add new tempchannels
    # make a way to remove tempchannels
    # make a way to list configured tempchannels
    
    grp_jointocreate = app_commands.Group(name="jointocreate", description="Gerencia a criação de canais de voz geradores de canais temporários")
    
    @grp_jointocreate.command(name="criar", description="Cria um canal JTC")
    @app_commands.describe(channel="ID do canal de voz")
    async def jtc_create(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await interaction.response.defer()
        channel_id = channel.id

        # Inserir os dados no banco de dados
        self.db.insert_one({
            'GUILD_ID': interaction.guild.id,  # ID do servidor
            'JTC_CHANNEL_ID': channel_id,      # ID do canal de voz
            'INVOKED_BY_USER_ID': interaction.user.id,  # ID do usuário que configurou
        })

        # Confirmar com o usuário
        await interaction.followup.send(
            f"O canal de voz **{channel.name}** foi configurado como um canal join-to-create!"
        )
        
    
    @grp_jointocreate.command(name="delete", description="Remove um canal JTC")
    @app_commands.describe(channel="ID do canal de voz")
    async def jtc_delete(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await interaction.response.defer()
        channel_id = channel.id
        
        # delete one by jtc channel id
        self.db.delete_one({
            'JTC_CHANNEL_ID': interaction.channel.id,
        })
        
        await interaction.response.send_message(f"O canal {interaction.channel.name} foi desconfigurado.")

# Configura o COG
async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
