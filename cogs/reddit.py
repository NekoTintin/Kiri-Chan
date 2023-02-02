# Bibliothèques de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

# Autres
from praw import Reddit as Red
import tools.passwords as pwrd

# Défini l'objet Reddit pour accéder au compte de Kirlia-Chan
wrapper = Red(
    # ID pour s'identifier en tant que Bot sur Reddit
    client_id = pwrd.reddit_id,
    client_secret = pwrd.reddit_secret,
    user_agent = "discord.py:kirlia-chan-bot:v3.0(by u/tintin361yt)",
    # ID du compte Reddit
    username = "Kirlia-chan",
    password = pwrd.reddit_password,
    # Pour éviter les messages chiants d'Async PRAW
    check_for_async = False)

class Reddit(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
        
    
    # Retourne de dernier post d'un subreddit dans un message Embed
    @app_commands.command(name="last", description="Affiche le dernier post d'un SubReddit.")
    async def last(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        

def get_post(sub: str, sort_type: str, limit: int):
    subreddit = wrapper.subreddit()