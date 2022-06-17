# -- coding: utf-8 --
# Biblio de Discord
from discord.ext import commands
from discord.embeds import Embed
# Module du bot
import kiri

class Tools(commands.Cog):
    
    # Méthode d'initialisation de la classe (avec bot an argument).
    def __init__(self, bot):
        self.bot = bot
        
    # Commandes Outils/Tools
    # Retourne la latence
    @commands.command(name="ping", aliases=["latence", "Latence"])
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"Pong ! - La latence est de: **{self.bot.latency * 1000}** millisecondes.")
    
    # Retourne la version
    @commands.command(name="version", aliases=['ver', 'botver'])
    async def version(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"Je suis en version: **{kiri.ver_num}** !")
    
    # Renvoie un lien vers le repo GitHub
    @commands.command(name="github", aliases=['GitHub', 'Github', 'gitHub', "git", "Git"])
    async def git(self, ctx):
        await ctx.message.delete()
        message = Embed(title="Lien du GitHub:", color=0xfbfcfc).add_field(name="Repo de Kiri-Chan:", value="https://github.com/Tintin361/Kiri-chan").add_field(name="Repo de Little Kyubey", value="https://github.com/Tintin361/Lil_Kyubey")
        await ctx.send(embed=message)
        
    # Aide pour les commandes Outils
    @commands.command(name="helpTools", aliases=["helptools", "helpOutils"])
    async def aideTools(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_tools())
        
def get_help_tools():
  embedMsg = Embed(title=":screwdriver: Outils", description="Liste des commandes pour les outils", color=0x99aab5)
  embedMsg.add_field(name="-ping", value="Affiche la latence")
  embedMsg.add_field(name="-version", value="Obtiens le numéro de version")
  embedMsg.add_field(name="-github", value="Lien vers le repo sur GitHub.")
  
  return embedMsg

# Fonction pour ajouter le cog
def setup(bot):
    bot.add_cog(Tools(bot))