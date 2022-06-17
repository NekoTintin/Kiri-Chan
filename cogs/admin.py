# Importation de bibliothèques
import discord
from discord.ext import commands
from discord.embeds import Embed

class Admin(commands.Cog):
    
    # Initialisation
    def __init__(self, bot):
        self.bot = bot
    
    # Delete Messages Function
    @commands.command(name="deleteMessage", aliases=['dlt', 'deletemessage', 'delete'])
    async def delete(self, ctx, id):
        await ctx.message.delete()
    
        channel = self.bot.get_channel(ctx.channel.id)
        message = await channel.fetch_message(int(id))
        await message.delete()
        
    # Shutdown the bot
    @commands.command(name="shutdown", aliases=['sd'])
    async def shutdown(self, ctx):
        await ctx.message.delete()
        try:
            await ctx.voice_client.disconnect()
        except:
            pass
        await self.bot.logout()

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
        
    # Aide pour les commandes Admin
    @commands.command(name="helpAdministratif", aliases=["helpAdmin", "helpadmin"])
    async def aideAdmin(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_admin())
        
def get_help_admin():
  embedMsg = Embed(title="<:Modo:945135154131791912> Administratif", description="Liste des commandes uniquement pour les modérateurs", color=0xff00fa)
  #embedMsg.add_field(name="-mpSet [ID utilisateur]", value="Permet de définir à qui j'envoie le Message Privé")
  #embedMsg.add_field(name="-mp [contenu du message]", value="J'envoie le contenu de ton message")
  embedMsg.add_field(name="-online [type] [message]", value="Je suis connectée")
  embedMsg.add_field(name="-idle [type] [message]", value="Je deviens inactive")
  embedMsg.add_field(name="-dnd [type] [message]", value="Ne me dérange pas")
  embedMsg.add_field(name="-invisible", value="Mais t'es pas là, mais t'es où ?")
  embedMsg.add_field(name="-shutdown", value="Arrêt du bot")

  return embedMsg
        
def setup(bot):
    bot.add_cog(Admin(bot))