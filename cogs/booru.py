import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

from pybooru import Danbooru
from random import choice
from secrets import token_hex
from tools.passwords import danbooru_api
from tools.variables import values

dan = Danbooru('danbooru', username="Kiri-chan27", api_key=danbooru_api)
safe = Danbooru('safebooru', username="Kiri-chan27", api_key=danbooru_api)

class Pybooru(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="safebooru", description="Recherche une image depuis le site Safebooru.")
    async def search_safebooru(self, interaction: discord.Interaction, nombre: values, tags: str):
        await interaction.response.defer(ephemeral=False)
        
        errors = 0
        for _ in range(nombre):
            try:
                img = choice(safe.post_list(tags=tags, limit=5000))
                             
                msg_color = discord.Color.from_str(f'#{token_hex(3)}')
                msg = Embed(title="Recherche sur Safebooru:", description=f"Avec les tags:\n**{tags}**", color=msg_color)
                msg.set_image(url=img['file_url'])
                msg.set_footer(text=f"Depuis Safebooru - ID {img['id']}", icon_url="https://i.pinimg.com/564x/1b/8a/82/1b8a82e579861ec8a0bfac7f378e2cce.jpg")
                
                view = discord.ui.View(timeout=None)
                view.add_item(discord.ui.Button(label="Lien vers l'image", style=discord.ButtonStyle.link, url=img['file_url']))
        
                await interaction.followup.send(embed=msg, view=view, ephemeral=False)
            except:
                errors += 1
                continue
            
        if errors > 0:
            await interaction.followup.send(f"Nombre d'images qui n'ont pas pu être affichées: {errors}.", ephemeral=True)
            
    @app_commands.command(name="danbooru", description="Recherche une image depuis le site Danbooru.")
    async def search_danbooru(self, interaction: discord.Interaction, nombre: values, tags: str):
        if not interaction.channel.is_nsfw():
            return await interaction.response.send_message("Cette commande est reservée à un salon NSFW.", ephemeral=True)
        await interaction.response.defer(ephemeral=False)
        
        errors = 0
        for _ in range(nombre):
            try:
                img = choice(dan.post_list(tags=tags, limit=5000))
                             
                msg_color = discord.Color.from_str(f'#{token_hex(3)}')
                msg = Embed(title="Recherche sur Danbooru:", description=f"Avec les tags:\n**{tags}**", color=msg_color)
                msg.set_image(url=img['file_url'])
                msg.set_footer(text=f"Depuis Danbooru - ID {img['id']}", icon_url="https://avatars.githubusercontent.com/u/57931572?s=280&v=4")
                
                view = discord.ui.View(timeout=None)
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