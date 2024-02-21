import discord
from discord.ext import commands
from discord.embeds import Embed
from datetime import datetime as dt
import pytz
import tools.variables as var
import platform
import tools.paths as paths

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
        print(f"Version du bot: {var.ver_num}")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=var.online_message))
        
        with open(f"{paths.data_path}list_of_channels.txt", "w") as file:
            pass
        with open(f"{paths.data_path}list_of_channels.txt", "a") as file:
            for guild in self.bot.guilds:
                file.write(f"---- {guild.name}:\n")
                for channel in guild.channels:
                    file.write(f"- {channel}\n")
        
        with open(f"{paths.data_path}list_of_user.txt", "w") as file:
            pass
        with open(f"{paths.data_path}list_of_user.txt", "a") as file:
            file.write("Liste des membres :\n\n")
            
            for guild in self.bot.guilds:
                file.write(f"Serveur : {guild.name}\n")
                
                for member in guild.members:
                    file.write(f"-- Nom: {member.name}\n")
                    file.write(f"    ID: {member.id}\n")
                    file.write(f"    Avatar: {member.avatar}\n")
                    file.write(f"    Rôles: {', '.join([role.name for role in member.roles])}\n")
                    file.write(f"    Membre depuis: {str(member.joined_at)}\n")
                file.write("\n")
        
    # Permet de charger un cog
    @commands.command(name="load")
    async def load(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.load_extension(f"cogs.{extention}")
        await ctx.bot.tree.sync()
        var.enable_module(extention)
        await ctx.send(f"Le module {extention} a bien été chargé")
        
    # Permet de décharger un cog
    @commands.command(name="unload")
    async def unload(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.unload_extension(f"cogs.{extention}")
        await ctx.bot.tree.sync()
        var.disable_module(extention)
        await ctx.send(f"Le module {extention} a bien été déchargé")
        
    # Permet de recharger un cog
    @commands.command(name="reload")
    async def reload(self, ctx, extention):
        await ctx.message.delete()
        await self.bot.unload_extension(f"cogs.{extention}")
        await self.bot.load_extension(f"cogs.{extention}")
        await ctx.bot.tree.sync()
        await ctx.send(f"Le module {extention} a bien été rechargé")
        
    # Envoie un message avec la liste des modules
    @commands.command(name="modules", aliases=['mod'])
    async def modules(self, ctx):
        message = f"Liste des modules:\n"
        mods = var.get_modules()
        for mod in mods:
            message += f"- **{mod}**: {mods[mod]}\n"
        await ctx.send(message)
        
    # Se déclenche à chaque message
    @commands.Cog.listener()
    async def on_message(self, message):
        msg_str = str(message.content)
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message) and message.mention_everyone == False:
            await message.channel.send(f"Hey {message.author.mention}, utilise **/** pour afficher la liste des commandes.")
            
        if msg_str == "":
            content = "[image]" 
        else:
            content = str(message.content)
            
        if "womp womp" in msg_str.lower():
            womp = Embed(title="WOMP WOMP !!!", color=0x800080)
            womp.set_image(url="https://media.tenor.com/13xUat9h3T4AAAAd/shylily-womp.gif")
            await message.channel.send(embed=womp)
            
        if "waku waku" in msg_str.lower():
            waku = Embed(title="WAKU WAKU !!!", color=0xee8281)
            waku.set_image(url="https://www.serieously.com/app/uploads/2022/06/anya.gif")
            await message.channel.send(embed=waku)
    
        username = await self.bot.fetch_user(message.author.id)
        with open (f"{paths.data_path}history.txt", "a") as hist:
            hist.write(f"{get_time()} - {username}: {content}\n")
        
        if message.channel.id == 935514239035142164:
            await message.delete()
            
    # Pour synchroniser les commandes slash
    @commands.command()
    async def sync(self, ctx, guild = None) -> None:
        if guild == None:
            fmt = await ctx.bot.tree.sync()
            await ctx.send(f"{len(fmt)} commandes ont été synchronisées.")
        else:
            ctx.bot.tree.copy()
        
async def setup(bot):
    await bot.add_cog(Begin(bot))