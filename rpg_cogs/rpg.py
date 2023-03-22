import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands, ui
from datetime import datetime
from random import choice, randint
from secrets import SystemRandom
import sqlite3
from sqlite3 import Error

user_list = [592750256899489825, 443113150599004161, 682217361092378671]
example_name = ["Jean le Ragondin", "Kot1 Le Faux", "Jean-Bernard de la Sainte Famille du Compté de...", "Truc", "Bernard Minet"]

"""
    self.identifiant = 592750256899489825
    self.name = "KOR1, THE SYMPATHIQUE DICTATOR !!!!"
    self.max_hp = 9999
    self.atk = 0.5
    self.defense = 0.69
    self.max_mp = 9999
"""

class Character_Modal(ui.Modal, title="C'est l'heure de créer ton PERSONNAGE !!!"):
    answer = ui.TextInput(label="Quel est ton nom de GUERRIER/GUERRIÈRE ?", style=discord.TextStyle.short, placeholder=choice(example_name), required=True, min_length=5)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        #await interaction.response.defer()
        database = sqlite3.connect("/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/data/rpgDB.db")
        cur = database.cursor()

        hp, mp, atk, defe = randint(1, 5), randint(1, 3), randint(1, 2), randint(0, 1)
        
        cur.execute("INSERT INTO players (player_discord_id, player_name, player_max_hp, player_max_mp, player_atk, player_def, player_is_dead, player_gold, player_power) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", ((int(interaction.user.id), str(self.answer), hp, mp, atk, defe, 0, 0, hp+mp+atk+defe)))
        database.commit()
        database.close()
        
        await interaction.response.send_message("Ton personnage a bien été créé !")
        
class Rpg(commands.GroupCog, name="rpg"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.guilds(759147102093049876)
    @app_commands.command(name="create", description="Crée ton personnage pour démarrer ton aventure.")
    async def create_character(self, interaction: discord.Interaction):
        if interaction.user.id not in user_list:
            await interaction.response.send_message("Tu ne peux pas utiliser cette commande.")

        database = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/data/rpgDB.db')
        cur = database.cursor()
        cur.execute("SELECT EXISTS(SELECT player_name FROM players WHERE player_discord_id=?)", (interaction.user.id,))
        if cur.fetchone()[0] == 0:
            await interaction.response.send_modal(Character_Modal())
        else:
            await interaction.response.send_message(content="Tu as déjà un personnage, pas la peine d'en créer un nouveau !", ephemeral=True)
        database.close()
    
    @app_commands.guilds(759147102093049876)
    @app_commands.command(name="stats", description="Consulte les statistiques de ton personnage.")
    async def stat(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id not in user_list:
            await interaction.response.send_message("Tu ne peux pas utiliser cette commande.")
            
        database = sqlite3.connect('/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/data/rpgDB.db')
        cur = database.cursor()
        cur.execute("SELECT player_name, player_max_hp, player_max_mp, player_atk, player_def, player_gold, player_power FROM players WHERE player_discord_id=? AND player_is_dead=0", (interaction.user.id,))
            
        data = cur.fetchone()
        
        msg = Embed(title=f"Statistiques de: {data[0]}", color=0x00ffe1)
        msg.add_field(name="HP Maximum:", value=f"**{data[1]}**")
        msg.add_field(name="MP Maximum:", value=f"**{data[2]}**")
        msg.add_field(name="Attaque:", value=f"**{data[3]}**")
        msg.add_field(name="Défense:", value=f"**{data[4]}**")
        msg.add_field(name="Or:", value=f"**{data[5]}**")
        msg.add_field(name="Niveau de Puissance:", value=f"**{data[6]}**")
        msg.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
        msg.set_footer(text="Kiri-chan: The Promised Neverlands of Jojo !", icon_url="https://images-ext-1.discordapp.net/external/7Yhla3kMaxtVKEFZIv9vOuDWsLeA8-pSvB2AFyYeNr4/%3Fsize%3D4096%26ignore%3Dtrue/https/cdn.discordapp.com/avatars/789984188224110632/b06507f8de4e4883b8fac4b2330cbb5b.png?width=634&height=634")
        msg.set_thumbnail(url="https://media.istockphoto.com/id/1223671392/fr/vectoriel/photo-de-profil-par-défaut-avatar-photo-placeholder-illustration-de-vecteur.jpg?s=170667a&w=0&k=20&c=EqD6q8IUqwN_bgGec0UBhh3tk2Zuur5lezDDlQsGdPY=")


        await interaction.followup.send(embed=msg, ephemeral=True)
                
        database.close()
        

async def setup(bot):
    await bot.add_cog(Rpg(bot))