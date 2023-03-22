import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

from pybooru import Danbooru
from secrets import token_hex, SystemRandom
from tools.passwords import danbooru_api
from tools.variables import values

dan = Danbooru('danbooru', username="Kiri-chan27", api_key=danbooru_api)
safe = Danbooru('safebooru', username="Kiri-chan27", api_key=danbooru_api)

class Posts_Button(discord.ui.View):
    
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="Ajouter à ta liste", style=discord.ButtonStyle.success, emoji="📝")
    async def add_to_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        id = interaction.user.id
        link = interaction.message.embeds[0].image.url
        
        try:
            with open(f"/home/Tintin/discord_bot/NekoBot/data/{id}.txt", "a") as file:
                file.write(f"{link}\n")
            await interaction.response.send_message("✅ Ajouté à ta liste !", delete_after=15, ephemeral=True)
            return
        except:
            await interaction.response.send_message("❌ Impossible de l'ajouter à la liste...", delete_after=15, ephemeral=True)
            return

class Pybooru(commands.GroupCog, name="pybooru"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.random = SystemRandom()
        super().__init__()

    @app_commands.command(name="safebooru", description="Recherche une image depuis le site Safebooru.")
    async def search_safebooru(self, interaction: discord.Interaction, nombre: values, tags: str):
        await interaction.response.defer(ephemeral=False)
        
        errors = 0
        for _ in range(nombre):
            try:
                img = self.random.choice(safe.post_list(tags=tags, limit=5000))
                             
                msg_color = discord.Color.from_str(f'#{token_hex(3)}')
                msg = Embed(title="Recherche sur Safebooru:", description=f"Avec les tags:\n**{tags}**", color=msg_color)
                msg.set_image(url=img['file_url'])
                msg.set_footer(text=f"Depuis Safebooru - ID {img['id']}", icon_url="https://i.pinimg.com/564x/1b/8a/82/1b8a82e579861ec8a0bfac7f378e2cce.jpg")
                
                view = Posts_Button(timeout=None)
                view.add_item(discord.ui.Button(label="Lien vers l'image", style=discord.ButtonStyle.link, url=img['file_url']))
        
                await interaction.followup.send(embed=msg, view=view, ephemeral=False)
            except:
                errors += 1
                continue
            
        if errors > 0:
            await interaction.followup.send(f"Nombre d'images qui n'ont pas pu être affichées: {errors}.", ephemeral=True)
            
    @app_commands.command(name="danbooru", description="Recherche une image depuis le site Danbooru.", nsfw=True)
    async def search_danbooru(self, interaction: discord.Interaction, nombre: values, tags: str):
        await interaction.response.defer(ephemeral=False)
        
        errors = 0
        for _ in range(nombre):
            try:
                img = self.random.choice(dan.post_list(tags=tags, limit=5000))
                             
                msg_color = discord.Color.from_str(f'#{token_hex(3)}')
                msg = Embed(title="Recherche sur Danbooru:", description=f"Avec les tags:\n**{tags}**", color=msg_color)
                msg.set_image(url=img['file_url'])
                msg.set_footer(text=f"Depuis Danbooru - ID {img['id']}", icon_url="https://avatars.githubusercontent.com/u/57931572?s=280&v=4")
                
                view = Posts_Button(Timeout=None)
                view.add_item(discord.ui.Button(label="Lien vers l'image", style=discord.ButtonStyle.link, url=img['file_url']))
        
                await interaction.followup.send(embed=msg, view=view, ephemeral=False)
            except:
                errors += 1
                continue
            
        if errors > 0:
            await interaction.followup.send(f"Nombre d'images qui n'ont pas pu être affichées: {errors}.", ephemeral=True)

# Fonction pour ajouter le cog
async def setup(bot):
    await bot.add_cog(Pybooru(bot))