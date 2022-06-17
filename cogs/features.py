# -- coding: utf-8 --
# Biblio de Discord
from discord.embeds import Embed
from discord.ext import commands
# Autres biblio
from datetime import datetime
from pytz import timezone
from random import randint

class Features(commands.Cog):
    
    # Méthode d'initialisation de la classe (avec bot an argument).
    def __init__(self, bot):
        self.bot = bot
        
    # Pourquoi ? Parce que
    @commands.command(name="poyo")
    async def poyo(self, ctx):
        await ctx.message.delete()
        await ctx.send("POYO !!!")
        
    # Affiche le jour et l'heure
    @commands.command(name="datetime")
    async def datetime(self, ctx):
        await ctx.message.delete()
        now = datetime.now(timezone('Europe/Paris'))
        time = now.strftime("%d/%m/%Y - %H:%M:%S")
        await ctx.send(f"On est le {time}")
        
    # Affiche un nombre aléatoire entre num1 et num2
    @commands.command(name="randomNum")
    async def randomNum(self, ctx, num1: int, num2: int):
        await ctx.message.delete()
        result = randint(num1, num2)
        await ctx.send(f"J'ai choisis le nombre: {result}")
        
    # Change le pseudo de Kiri-chan sur le serveur
    @commands.command(name="pseudo")
    async def pseudo(self, ctx, *arg):
        await ctx.message.delete()
        name = ' '.join(arg)
        await ctx.guild.get_member(self.bot.user.id).edit(nick=name)
        await ctx.send(f'Mon nouveau pseudo c\'est: **{name}**')
        
    # Change le pseudonyme de l'utilisateur
    @commands.command(name="nick")
    async def nick(self, ctx, *pseudo):
        await ctx.message.delete()
        name = ' '.join(pseudo)
        user = await ctx.guild.fetch_member(ctx.message.author.id)
        try:
            await user.edit(nick=pseudo)
        except:
            await ctx.send("Désolée, je ne peux pas changer ton pseudo, je n'ai pas les permissions... :confused:")
            return
        await ctx.send(f"{ctx.author.mention} J\'ai changé ton pseudo, c\'est maintenant: **{name}** !")
        
    # Aide pour les commandes Features
    @commands.command(name="helpFeatures", aliases=["helpfeatures"])
    async def aideFea(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_features())

def get_help_features():
  embedMsg = Embed(title=":robot: Features", description="Liste des commandes pour les features", color=0xed8a09)
  embedMsg.add_field(name="-poyo", value="POYO !")
  embedMsg.add_field(name="-pseudo [pseudonyme]", value="Change mon pseudo")
  embedMsg.add_field(name="-nick [pseudonyme]", value="Change ton pseudo si j'ai les permissions")
  embedMsg.add_field(name="-datetime", value="Je te donne l'heure")
  embedMsg.add_field(name="-randomNum [valeur 1] [valeur 2]", value="Je te donne un nombre aléatoire entre deux valeurs")

  return embedMsg  
        
# Fonction pour ajouter le cog
def setup(bot):
    bot.add_cog(Features(bot))