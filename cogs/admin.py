# Bibliothèques de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

# Autres Biblio
import tools.variables as var
from typing import Literal

class Admin(commands.Cog):
    
    # Initialisation
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    """   
    # Commande pour gérer le statut du Bot
    @app_commands.command(name="status", description="Défini le status du Bot.")
    async def statut(self, interaction: discord.Interaction, statut: Literal["En ligne", "Absent", "Ne pas déranger", "Invisible"], activité: Literal["Joue à", "Écoute", "Regarde"], message: str):
        status_state = {"En ligne": discord.Status.online, "Absent": discord.Status.idle, "Ne pas déranger": discord.Status.dnd, "Invisible": discord.Status.invisible}
        activity_state = {"Joue à": discord.Game(name=message), "Écoute": discord.Activity(type=discord.ActivityType.listening, name=message), "Regarde": discord.Activity(type=discord.ActivityType.watching, name=message)}
        
        try:
            await self.bot.change_presence(statut=status_state[statut], activity=activity_state[activité])
        except:
            await interaction.response.send_message("No", delete_after=5)
            return
        await interaction.response.send_message("yes", delete_after=5)

    @commands.command(name="online")
    async def online(self, ctx, activity="watch", *msg):
        await ctx.message.delete()
        message = ' '.join(msg)
        if message == None:
            message = ""
    
        activity = activity.lower()
        if activity == "watch" or activity == "watching":
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif activity == "listen":
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif activity == "game":
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=message))

    @commands.command(name="idle")
    async def idle(self, ctx, activity="watch", *msg):
        await ctx.message.delete()
        message = ' '.join(msg)
        if message == None:
            message = "Splatoon 2 ou à Pokémon"
    
        activity = activity.lower()
        if activity == "watch" or activity == "watching":
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif activity == "listen":
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif activity == "game":
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=message))

    @commands.command(name='dnd', aliases=['doNotDisturb', 'donotDisturb', 'donotdisturb'])
    async def dnd(self, ctx, activity="watch", *msg):
        await ctx.message.delete()
        message = ' '.join(msg)
        if message == None:
            message = "un anime (c\'est sympa Assassination Classroom !)"
    
        activity = activity.lower()
        if activity == "watch" or activity == "watching":
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif activity == "listen":
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif activity == "game":
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=message))

    @commands.command()
    async def invisible(self, ctx):
        await ctx.message.delete()
        await self.bot.change_presence(status=discord.Status.invisible)
    """

        
async def setup(bot):
    await bot.add_cog(Admin(bot))