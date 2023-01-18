# En cours de développement
import discord
from discord.ext import commands
from discord.embeds import Embed
from pybooru import Danbooru
from pybooru import Moebooru

class Booru(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.safe = Danbooru('safebooru')

    @commands.command(name="search_safebooru", aliases=['safe'])
    async def search_safebooru(self, ctx, *search):
        query = ' '.join(search)
        posts = self.safe.post_list(tags=query, limit=1)
        for post in posts:
            await ctx.send(post['file_url'])
            
    @commands.command(name="konachan")
    async def notsafe(self, ctx, *search):
        booru = Moebooru('konachan')
        query = ' '.join(search)
        posts = booru.post_list(tags=query, limit=1)
        for post in posts:
            await ctx.send(post['file_url'])
            
    # Aide pour les commandes Admin
    @commands.command(name="helpBooru", aliases=["helpbooru"])
    async def aideBooru(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_booru())
    
def get_help_booru():
  embedMsg = Embed(title=":desktop: Booru", description="['Booru description']", color=0xff00fa)
  embedMsg.add_field(name="-safe [tag]", value="Recherche depuis Safebooru")

  return embedMsg

# Fonction pour ajouter le cog
async def setup(bot):
    await bot.add_cog(Booru(bot))