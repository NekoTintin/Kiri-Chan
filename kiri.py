# Importation de bibliothèques de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
# Bibliothèques pour Linux
import os
# Modules avec tous les mots de passe [que vous ne pouvez pas voir :)].
import tools.passwords as pwrd

# Variable pour le bot
ver_num = "2.0.5"
online_message = "Hiii !!!!"
# Dictionnaire qui stocke les cogs chargés
loaded_ext = dict()

# Charge les intents par défaut
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)

# Fonction pour obtenir les modules chargés
def get_modules() -> list():
    l = list()
    for filename in loaded_ext:
        if loaded_ext[filename] == True:
            l.append(filename)
    return l

@bot.command(name="modules", aliases=['mod'])
async def modules(ctx):
    message = f"Liste des modules chargés:\n"
    for mod in get_modules():
        message += f"- *{mod}*\n"
    await ctx.send(message)


# Permet de charger un module (Cog) dans ./cogs/
@bot.command()
async def load(ctx, extensions):
    await ctx.message.delete()
    bot.load_extension(f'cogs.{extensions}')
    loaded_ext[extensions] = True

# Permet de décharger un module (Cog) dans ./cogs/ 
@bot.command()
async def unload(ctx, extensions):
    await ctx.message.delete()
    bot.unload_extension(f'cogs.{extensions}')
    loaded_ext[extensions] = False
    
# Permet de recharger un module (Cog) dans ./cogs/ 
@bot.command()
async def reload(ctx, extensions):
    await ctx.message.delete()
    bot.unload_extension(f'cogs.{extensions}')
    loaded_ext[extensions] = False
    bot.load_extension(f'cogs.{extensions}')
    loaded_ext[extensions] = True
    
# On charge tous les modules au démarre du bot
for filename in os.listdir('/home/Tintin/Desktop/Kiri-chan/cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')
        loaded_ext[filename[:-3]] = True
        
# Erreur de commande
@bot.event
async def on_command_error(ctx, error):
    print(error)
    emd = Embed(title="<:Erreur:945123023546093611> Commande inconnue", description="Désolée, je ne connais pas cette commande ou celle-ci a plantée...", color=0xe24647).add_field(name="Sortie:", value=str(error), inline=False)
    await ctx.channel.send(embed=emd)

# YATTA - Démarre le bot
bot.run(pwrd.bot_token)