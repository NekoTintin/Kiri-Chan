# Importation de bibliothèques de Discord
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
# Bibliothèques
import os
#import sqlite3
from secrets import token_hex
from validators import url as test_url
# Modules avec tous les mots de passe [que vous ne pouvez pas voir :)].
import tools.passwords as pwrd
import tools.variables as var

# Variable pour le bot
ver_num = var.ver_num
online_message = var.online_message

# Charge les intents par défaut
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="-", owner_ids=set(pwrd.owner), help_command=None, intents=intents)

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
    
# Quand le bot rejoint un serveur
@bot.event
async def on_guild_join(ctx, guild: discord.Guild) -> None:
    await ctx.bot.tree.sync()
    print(f"Bot ajouté sur le serveur {guild.name}")

"""
async def _user_stat(react: discord.Interaction, user: discord.Member):
    database = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/data/rpgDB.db')
    cur = database.cursor()
    cur.execute("SELECT EXISTS(SELECT player_name FROM players WHERE player_discord_id=?)", (user.id,))
    if cur.fetchone()[0] == 0:
        return await react.response.send_message("Cet utilisateur ne possède pas de personnage.", ephemeral=True)

    cur.execute("SELECT player_name, player_power FROM players WHERE player_discord_id=? AND player_is_dead=0", (user.id,))
    data = cur.fetchone()
        
    await react.response.send_message(content=f"**{data[0]}**, personnage de {user.mention} possède un Niveau de Puissance de: {data[1]}.", ephemeral=True)

class Credit_Modal(discord.ui.Modal):
    
    def __init__(self, title: str = "Crédit Sociaux") -> None:
        self.user_target = user_target
        self.nb_credit = discord.ui.TextInput(label="Entre un nombre.", placeholder=426662912, min_length=1, required=True)
        super().__init__(title=title)
    
    async def on_submit(self, react: discord.Interaction):
        try:
            nb_credit_int = int(self.nb_credit.value)
        except TypeError:
            return await react.response.send_message("Entre un nombre valide, Grand Dictateur.", ephemeral=True)
        
        db = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/data/user_data.db')
        cur = db.cursor()
        cur.execute("SELECT EXISTS(SELECT credit_value FROM credits WHERE user_id=?)", (self.user_target,))
        db.commit()
        data = cur.fetchone()
    
        if data[0] == 0:
            await react.response.send_message(f"Cet utilisateur possède maintenant {self.nb_credit.value} crédits.", ephemeral=True)
            cur.execute("INSERT INTO credits VALUES (?, ?)", (self.user_target, nb_credit_int))
            db.commit()
            db.close()
            return
    
        await react.response.send_message(f"Cet utilisateur possède maintenant {self.nb_credits} crédits.", ephemeral=True)
        cur.execute("UPDATE credits SET credit_value=? WHERE user_id=?", (nb_credit_int, self.user_target))
        db.commit()
        db.close()
    

async def _change_social_credit(react: discord.Interaction, user: discord.Member):
    list_mod = [592750256899489825, 443113150599004161]
    if react.user.id not in list_mod:
        return await react.response.send_message("Seul le Dictateur Sympathique peut modifier le nombre de crédits sociaux.", ephemeral=True)
    
    if user.bot:
        return await react.response.send_message("Les bots ne possèdent pas de crédits.", ephemeral=True)
    elif user.id == 592750256899489825:
        return await react.response.send_message("Le dictateur Kor1 ne peut pas avoir de crédits sociaux.", ephemeral=True)
    elif user.id == 443113150599004161:
        return await react.response.send_message("J'ai oubliée ta requête, désolée... 😅", ephemeral=True)
    
    await react.response.send_modal(Credit_Modal(user.id))
    
    
async def _view_social_credits(react: discord.Interaction, user: discord.Member):
    if user.bot:
        return await react.response.send_message("Les bots ne possèdent pas de crédits.", ephemeral=True)
    elif user.id == 592750256899489825:
        return await react.response.send_message("Le dictateur Kor1 ne peut pas avoir de crédits sociaux.", ephemeral=True)
    elif user.id == 443113150599004161:
        return await react.response.send_message("J'ai oubliée ta requête, désolée... 😅", ephemeral=True)
    
    database = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/data/user_data.db')
    cur = database.cursor()
    cur.execute("SELECT EXISTS(SELECT credit_value FROM credits WHERE user_id=?)", (user.id,))
    database.commit()
    data = cur.fetchone()
    
    if data[0] == 0:
        await react.response.send_message(f"{user.mention} possède 0 crédits.", ephemeral=True)
        cur.execute("INSERT INTO credits VALUES (?, ?)", (user.id, 0))
        database.commit()
        database.close()
        return
    
    database.close()
    return await react.response.send_message(f"{user.mention} possède {data[1]} crédit(s).", ephemeral=True)


user_stat_menu = app_commands.ContextMenu(name="Niveau de Puissance", callback=_user_stat)
view_social_credit = app_commands.ContextMenu(name="Voir les Crédits Sociaux", callback=_view_social_credits)
credit_menu = app_commands.ContextMenu(name="Changer les Crédits Sociaux", callback=_change_social_credit)


bot.tree.add_command(user_stat_menu)
bot.tree.add_command(view_social_credit)
bot.tree.add_command(credit_menu)
"""

async def _multipost(react: discord.Interaction, msg: discord.Message):
    options = list()
    for guild in bot.guilds:
        if react.user not in guild.members:
            break
        for channel in guild.channels:
            if any(word in channel.name.lower() for word in var.keywords) and react.channel_id != channel.id:
                options.append(discord.SelectOption(
                    label=channel.name,
                    description=f"Dans le serveur: {guild.name}",
                    value=f'{channel.id}',))

    select_menu = discord.ui.Select(options=options, placeholder="Choisis le(s) salon(s).", min_values=1, max_values=len(options))

    async def callback(react):
        await react.response.defer(ephemeral=True)
        for val in select_menu.values:
            emb = Embed(title=msg.content, color=discord.Color.from_str(f'#{token_hex(3)}'))
            if msg.attachments != []:
                emb.set_image(url=msg.attachments[0].url)
            elif test_url(msg.content):
                emb.set_image(url=msg.content)
            emb.set_author(name=msg.author.name, icon_url=msg.author.avatar.url)
            emb.set_footer(text=f"Depuis {bot.user.display_name} via la commande multipost.", icon_url=bot.user.avatar.url)
            await bot.get_channel(int(val)).send(embed=emb)
        await react.followup.send(content="Tout a été envoyé !", ephemeral=True)

    select_menu.callback = callback
    v = discord.ui.View()
    v.add_item(select_menu)
    await react.response.send_message(view=v, delete_after=180, ephemeral=True, allowed_mentions=False)


message_menu = app_commands.ContextMenu(name="Publier sur d'autres serveurs", callback=_multipost)
bot.tree.add_command(message_menu)

# Démarre le bot
asyncio.run(main(bot))