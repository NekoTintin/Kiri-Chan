# Biblio de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
# Module du bot
from tools import passwords
# Module Tweepy
import tweepy as tpy


tw_api_key = passwords.tw_api_key
tw_secret_key = passwords.tw_secret_key
tw_access_token = passwords.tw_access_token
tw_secret_token = passwords.tw_secret_token

auth = tpy.OAuthHandler(tw_api_key, tw_secret_key)
auth.set_access_token(tw_access_token, tw_secret_token)

api = tpy.API(auth)

class Twitter(commands.Cog):
    
    # Méthode d'initialisation de la classe (avec bot an argument).
    def __init__(self, bot):
        self.bot = bot
        
    # Tweet le message msg avec le compte avec le compte @Kirlia-Chan
    @commands.command(name="tweet")
    async def tweet(self, ctx, *msg):
        await ctx.message.delete()
        if ctx.message.author == 443113150599004161:
            message = ' '.join(msg)
            api.update_status(message)
        
    # Affiche la timeline du compte @Kirlia-Chan
    @commands.command(name="timeline", aliases=["tl"])
    async def tl(self, ctx):
        timeline = get_timeline()
        embed = discord.Embed(title="Timeline", color=0x1a8cd8)
        for user, content in timeline.items():
            embed.add_field(name=f"Tweet de {user}", value=content, inline=False)

        await ctx.send(embed=embed)
        
    # Aide pour les commandes Twitter
    @commands.command(name="helpTwitter")
    async def aideTwitter(self, ctx):
        await ctx.message.delete()
        
        embedMsg = Embed(title="<a:Twitter:945123022329741332> Twitter", description="Liste des commandes pour Twitter", color=0x6cb8e4)
        embedMsg.add_field(name="-tweet", value="Tweet avec le compte de @Kirlia-chan")
        embedMsg.add_field(name="-timeline", value="Affiche les trois derniers tweet de la timeline du compte @Kirlia-Chan")
        await ctx.send(embed=embedMsg)

def get_timeline():
    timeline = api.home_timeline()
    tl_list = {}
    for tweet in timeline:
        tl_list[tweet.user.name] = tweet.text
    return tl_list

# Fonction pour ajouter le cog
def setup(bot):
    bot.add_cog(Twitter(bot))