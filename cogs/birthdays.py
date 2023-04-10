import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput
import sqlite3
import re
from datetime import datetime as dt
from pytz import timezone

IST = timezone('Europe/Paris')

class Birthday_Modal(Modal, title="Défini ta date d'anniversaire"):
    date = TextInput(label="Entre ta date d'anniversaire !", style=discord.TextStyle.short, placeholder="01/05/2015", required=True, min_length=10, max_length=10)
    
    async def on_submit(self, react: discord.Interaction) -> None:
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', self.date.value):
            return await react.response.send_message("La date n'est pas valide.", ephemeral=True)
        
        execute_database(query="""INSERT INTO birthdays (discord_id, user_date) VALUES (?, ?)""", is_insert=True, data=[react.user.id, self.date.value])
        await react.response.send_message(f"La date a bien été enregistrée, tu es né(e) le **{self.date.value}**.", ephemeral=True)
        

class Birthday(commands.GroupCog, name="birthday"):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.b_list = self.get_b_list()
        bot.loop.create_task(self.check_birthdays())
        super().__init__()
        
    @app_commands.command(name="define", description="Défini ta date d'anniversaire")
    async def _define(self, react: discord.Interaction):
        await self.bot.wait_until_ready()
        for i in self.b_list:
            if react.user.id == i[0]:
                return await react.response.send_message("Tu as déjà défini ta date d'anniversaire !", ephemeral=True)
        await react.response.send_modal(Birthday_Modal())

    @app_commands.command(name="display", description="Affiche la date d'anniversaire d'un utilisateur.")
    async def _display(self, react: discord.Interaction, user: discord.User):
        await self.bot.wait_until_ready()
        for i in self.b_list:
            if user.id == i[0]:
                return await react.response.send_message(f"{user.name} est né(e) le **{i[1]}**.", ephemeral=True)
        await react.response.send_message(f"{user.name} n'a pas défini de date d'anniversaire.", ephemeral=True)
        
    async def check_birthdays(self):
        await self.bot.wait_until_ready()
        now = dt.now(IST)
        
        list = execute_database(query="""SELECT discord_id, user_date FROM birthdays""", is_insert=False)
        for user_data in list:
            day = user_data[1][:2]
            month = user_data[1][3:5]
            year = user_data[1][6:]
            
            if dt(int(now.year), int(month), int(day)).date() == now.date():
                user = self.bot.get_user(user_data[0])

                list_of_channels = []
                for guild in self.bot.guilds:
                    if user == guild.get_member(user_data[0]):
                        channels = guild.text_channels
                        list_of_channels.append(channels[0])
                
                for channel in list_of_channels:
                    await channel.send(f"Hey @everyone !\n{user.mention} fête son anniversaire aujourd'hui !\n{user.display_name} a maintenant {now.year - int(year)} ans.\nhttps://tenor.com/fr/view/im-old-mister-j-day-je-suis-vieux-j-day-vieux-gif-17846810")

    def get_b_list(self):
        database = sqlite3.connect("/home/Tintin/discord_bot/Kiri-chan/data/user_data.db")
        cur = database.cursor()
        cur.execute("""SELECT discord_id, user_date FROM birthdays""")
        database.commit()
        response = cur.fetchall()
        database.close()
        return response
        
def execute_database(query: str, is_insert: bool, data: list() = None) -> list() or None:
    database = sqlite3.connect("/home/Tintin/discord_bot/Kiri-chan/data/user_data.db")
    cur = database.cursor()
    if is_insert:
        cur.execute(query, (data[0], data[1]))
        database.commit()
        database.close()
        return
    cur.execute(query)
    database.commit()
    response = cur.fetchall()
    database.close()
    return response
        
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))