# -- coding: utf-8 --
# Biblio de Discord
import discord
from discord.ext import commands
from discord import app_commands
# Autres biblio
from datetime import datetime
from pytz import timezone
from random import randint

class Features(commands.GroupCog, name="features"):
    
    # Méthode d'initialisation de la classe (avec bot en argument).
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    # Pourquoi ? Parce que !
    @app_commands.command(name="poyo", description="Poyo !")
    async def poyo(self, interaction: discord.Interaction):
        await interaction.response.send_message("POYO !!!", ephemeral=True)
        
    # Affiche le jour et l'heure
    @app_commands.command(name="datetime", description="Affiche le Jour et l'Heure actuel.")
    async def datetime(self, interaction: discord.Interaction):
        now = datetime.now(timezone('Europe/Paris'))
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")
        await interaction.response.send_message(f"On est le {date} et il est {time}.")
        
    # Affiche un nombre aléatoire entre num1 et num2
    @app_commands.command(name="randomnum", description="Renvoie un nombre aléatoire.")
    async def randomNum(self, interaction: discord.Interaction, nombre1: int, nombre2: int):
        result = randint(nombre1, nombre2)
        await interaction.response.send_message(f"J'ai choisi le nombre: {result}.")
        
# Fonction pour ajouter le cog
async def setup(bot):
    await bot.add_cog(Features(bot))