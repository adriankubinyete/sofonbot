import logging
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger("sofonbot.command.informativos")

class Informativos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.informativos = []  # Lista para armazenar os informativos temporariamente
        
    # Grupo de comandos "informativos"
    grp_informativos = app_commands.Group(name="informativo", description="Gerencie informativos")

    @grp_informativos.command(name="criar", description="Cria um novo informativo.")
    async def criar(self, interaction: discord.Interaction, titulo: str, conteudo: str):
        """Cria um novo informativo."""
        self.informativos.append({"titulo": titulo, "conteudo": conteudo})
        logger.info(f"Informativo criado: {titulo}")
        await interaction.response.send_message(f"Informativo '{titulo}' criado com sucesso!", ephemeral=True)

    @grp_informativos.command(name="deletar", description="Deleta um informativo existente.")
    async def deletar(self, interaction: discord.Interaction, titulo: str):
        """Deleta um informativo pelo título."""
        informativo = next((i for i in self.informativos if i["titulo"] == titulo), None)
        if informativo:
            self.informativos.remove(informativo)
            logger.info(f"Informativo deletado: {titulo}")
            await interaction.response.send_message(f"Informativo '{titulo}' deletado com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Informativo '{titulo}' não encontrado.", ephemeral=True)

    @grp_informativos.command(name="listar", description="Lista todos os informativos.")
    async def listar(self, interaction: discord.Interaction):
        """Lista todos os informativos disponíveis."""
        if not self.informativos:
            await interaction.response.send_message("Nenhum informativo encontrado.", ephemeral=True)
        else:
            mensagem = "Informativos disponíveis:\n" + "\n".join(
                [f"- {i['titulo']}" for i in self.informativos]
            )
            await interaction.response.send_message(mensagem, ephemeral=True)

    async def cog_load(self):
        # Não é necessário adicionar o grupo de comandos manualmente
        pass

    async def cog_unload(self):
        # Remove o grupo de comandos ao descarregar o cog
        self.bot.tree.remove_command(self.grp_informativos.name, type=app_commands.CommandType.chat_input)

async def setup(bot):
    await bot.add_cog(Informativos(bot))
