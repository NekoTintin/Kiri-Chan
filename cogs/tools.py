# -- coding: utf-8 --
# Biblio de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands
# Module du bot
import tools.variables as var

class Tools(commands.GroupCog, name="tools"):
    
    # Méthode d'initialisation de la classe (avec bot an argument).
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
    # Commandes Outils/Tools
    # Retourne la latence
    @app_commands.command(name="ping", description="Affiche la latence.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong ! - La latence est de: **{self.bot.latency * 1000}** millisecondes.", ephemeral=True)
    
    # Retourne la version
    @app_commands.command(name="version", description="Obtiens le numéro de version")
    async def version(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Je suis en version: **{var.ver_num}** !", ephemeral=True)
    
    # Renvoie un lien vers le repo GitHub
    @app_commands.command(name="github", description="Lien vers le repo sur GitHub.")
    async def git(self, interaction: discord.Interaction):
        message = Embed(title="Lien du GitHub:", color=0xfbfcfc).add_field(name="Repo de Kiri-Chan:", value="https://github.com/Tintin361/Kiri-chan")\
        .add_field(name="Repo de Little Kyubey", value="https://github.com/Tintin361/Lil_Kyubey")\
        .add_field(name="Repo de NekoBot", value="https://github.com/Tintin361/NekoBot")
        await interaction.response.send_message(embed=message, ephemeral=True)

# Fonction pour ajouter le cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tools(bot))