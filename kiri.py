# Importation de bibliothèques de Discord
import discord
import asyncio
from discord.ext import commands
from discord.embeds import Embed
# Bibliothèques pour Linux
import os
# Modules avec tous les mots de passe [que vous ne pouvez pas voir :)].
import tools.passwords as pwrd
import tools.variables as var

# Variable pour le bot
ver_num = var.ver_num
online_message = var.online_message

# Charge les intents par défaut
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)

@bot.command()
async def main(bot):
    async with bot:
        for filename in os.listdir("/home/Tintin/discord_bot/Kiri-chan/cogs/"):
            if filename.endswith(".py") and filename != "reddit2.py":
                await bot.load_extension(f"cogs.{filename[:-3]}")
                var.add_module(filename[:-3])
        await bot.start(pwrd.bot_token)
        
# Erreur de commande
@bot.event
async def on_command_error(ctx, error):
    print(error)
    emd = Embed(title="<:Erreur:945123023546093611> Commande inconnue", description="Désolée, je ne connais pas cette commande ou celle-ci a plantée...", color=0xe24647).add_field(name="Sortie:", value=str(error), inline=False)
    await ctx.channel.send(embed=emd)

# Démarre le bot
asyncio.run(main(bot))