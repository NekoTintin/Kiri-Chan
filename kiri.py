# Importation de bibliothèques de Discord
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
# Bibliothèques pour Linux
import os
import sqlite3
# Modules avec tous les mots de passe [que vous ne pouvez pas voir :)].
import tools.passwords as pwrd
import tools.variables as var

# Variable pour le bot
ver_num = var.ver_num
online_message = var.online_message

# Charge les intents par défaut
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="-", owner_ids= set(pwrd.owner), help_command=None, intents=intents)

@bot.command()
async def main(bot):
    async with bot:
        for filename in os.listdir("/home/Tintin/discord_bot/Kiri-chan/cogs/"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                var.add_module(filename[:-3])
        for filename in os.listdir("/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/"):
            if filename.endswith(".py"):
                await bot.load_extension(f"rpg_cogs.{filename[:-3]}")
                var.add_module(filename[:-3])
        await bot.start(pwrd.bot_token)
  
# Erreur de commande
@bot.event
async def on_command_error(ctx, error):
    print(error)
    emd = Embed(title="<:Erreur:945123023546093611> Commande inconnue", description="Désolée, je ne connais pas cette commande ou celle-ci a plantée...", color=0xe24647).add_field(name="Sortie:", value=str(error), inline=False)
    await ctx.channel.send(embed=emd)

####
async def user_stat(interaction: discord.Interaction, user: discord.Member):
    database = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/data/rpgDB.db')
    cur = database.cursor()
    cur.execute("SELECT EXISTS(SELECT player_name FROM players WHERE player_discord_id=?)", (user.id,))
    if cur.fetchone()[0] == 0:
        return await interaction.response.send_message("Cet utilisateur ne possède pas de personnage.", ephemeral=True)

    cur.execute("SELECT player_name, player_power FROM players WHERE player_discord_id=? AND player_is_dead=0", (user.id,))
    data = cur.fetchone()
        
    await interaction.response.send_message(content=f"**{data[0]}**, personnage de {user.mention} possède un Niveau de Puissance de: {data[1]}.", ephemeral=True)


user_stat_menu = app_commands.ContextMenu(name="Niveau de Puissance", callback=user_stat)
bot.tree.add_command(user_stat_menu)


# Démarre le bot
asyncio.run(main(bot))