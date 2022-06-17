import discord
from discord.ext import commands
from discord.embeds import Embed
from datetime import datetime as dt
import pytz
import kiri
import platform

def write_in_txt(content, file):
    with open(file, "w") as f:
        f.write(str(content))
        
def get_time():
    now = dt.now(pytz.timezone('Europe/Paris'))
    time = now.strftime("%d/%m/%Y - %H:%M:%S")

    return time
  
class Begin(commands.Cog):
    # Fonction d'initialisation
    def __init__(self, bot) -> None:
        self.bot = bot
        
    # Se déclenche quand le bot est prêt
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Kiri-chan prête !")
        print(f"Version Python: {platform.python_version()}")
        print(f"Version Discord.py: {discord.__version__ }")
        print(f"Version du bot: {kiri.ver_num}")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=kiri.online_message))
        
    # Se déclenche à chaque message
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message) and message.mention_everyone == False:
            await message.channel.send(f"Hey {message.author.mention}, utilise **-help** pour afficher la liste des commandes.")
            
        if str(message.content) == "":
            content = "[image]" 
        else:
            content = str(message.content)
    
        username = await self.bot.fetch_user(message.author.id)
        hist = open("history.txt", "a")
        hist.write(get_time() + " - " + str(username) + ": " + content + "\n")
    
    # Affichage de la liste des commandes
    # Commande générale
    @commands.command(name="help", aliases=["aide"])
    async def aide(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help(kiri.get_modules()))
        
def get_help(mod):
  embedMsg = Embed(title="Liste des commandes", description="Liste de toutes les catégories", color=0xffffff)
  
  if "reddit" in mod:
    embedMsg.add_field(name="<:reddit:794069835138596886> Reddit", value="-helpReddit", inline=False)
  if "youtube" in mod: 
    embedMsg.add_field(name="<:youtube:316620060221374466> Youtube", value="-helpYoutube", inline=False)
  if "twitter" in mod: 
    embedMsg.add_field(name="<a:Twitter:945123022329741332> Twitter", value="-helpTwitter", inline=False)
  if "booru" in mod: 
    embedMsg.add_field(name=":desktop: Booru", value="-helpBooru", inline=False)
  if "features" in mod:
    embedMsg.add_field(name=":robot: Features", value="-helpFeatures", inline=False)
  if "tools" in mod:
    embedMsg.add_field(name=":screwdriver: Outils", value="-helpTools", inline=False)
  if "admin" in mod:
    embedMsg.add_field(name="<:Modo:945135154131791912> Administratif", value="-helpAdmin", inline=False)

  return embedMsg
        
def setup(bot):
    bot.add_cog(Begin(bot))