import discord
from discord.ext import commands
from discord import app_commands

import utils.danbooru_utils as dan_utils
from tools.variables import values, nsfw_values

class Pybooru(commands.Cog, name="pybooru"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="danbooru", description="Recherche une image depuis le site Danbooru.")
    async def search_safebooru(self, react: discord.Interaction, nombre: values, nsfw: bool, tags: str):
        await self.bot.wait_until_ready()
        await react.response.defer(ephemeral=False)
        
        if nsfw and not react.channel.is_nsfw():
            return await react.followup.send("Pour afficher du NSFW, mets-toi dans un salon NSFW.")
        
        try:
            result = dan_utils.search_on_danbooru("Recherche:", "Une image depuis Danbooru.", tags, nombre, nsfw_values[nsfw])
        except:
            return await react.followup.send(f"Aucun résultat n'a été trouvé... Vérifie que tes tags soient corrects: **{tags}**")
        
        if result is None:
            return await react.followup.send("Danbooru ne permet pas de faire des recherches de plus de 2 tags.")
        
        await react.followup.send(embed=result[0], view=result[1])

# Fonction pour ajouter le cog
async def setup(bot):
    await bot.add_cog(Pybooru(bot))