import discord
from discord.ext import commands
from discord import app_commands

import utils.danbooru_utils as dan_utils
from tools.variables import values

class Pybooru(commands.GroupCog, name="pybooru"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="safebooru", description="Recherche une image depuis le site Safebooru.")
    async def search_safebooru(self, react: discord.Interaction, nombre: values, tags: str):
        await self.bot.wait_until_ready()
        await react.response.defer(ephemeral=False)
        if not react.channel.is_nsfw():
            return await react.followup.send("Cette commande peut envoyer du contenu NSFW, envoie-la dans un salon ou il est activé.")
        
        result = dan_utils.search_on_danbooru("Recherche:", "Une image depuis Safebooru.", tags, nombre, "safebooru")
        if result == IndexError:
            return await react.followup.send(f"Aucun résultat trouvé, vérifie que ton tag est correct: *{tags}*")
        elif result is None:
            return await react.followup.send("Safebooru ne permet pas de faire des recherches de plus de 2 tags.")
        
        for key, value in result.items():
            if key == "errors":
                continue
            await react.followup.send(embed=value[0], view=value[1])
        if result["errors"] > 0:
            await react.followup.send(content=f"Nombre d'images qui n'ont pas pu être affichées: {result['errors']}.", ephemeral=True)
    
            
    @app_commands.command(name="danbooru", description="Recherche une image depuis le site Danbooru.", nsfw=True)
    async def search_danbooru(self, react: discord.Interaction, nombre: values, tags: str):
        await self.bot.wait_until_ready()
        await react.response.defer(ephemeral=False)
        if not react.channel.is_nsfw():
            return await react.followup.send("Cette commande peut envoyer du contenu NSFW, envoie-la dans un salon ou il est activé.")
        
        result = dan_utils.search_on_danbooru("Recherche:", "Une image depuis Danbooru.", tags, nombre, "danbooru")
        if result == IndexError:
            return await react.followup.send(f"Aucun résultat trouvé, vérifie que ton tag est correct: *{tags}*")
        elif result is None:
            return await react.followup.send("Danbooru ne permet pas de faire des recherches de plus de 2 tags.")
        
        for key, value in result.items():
            if key == "errors":
                continue
            await react.followup.send(embed=value[0], view=value[1])
        if result["errors"] > 0:
            await react.followup.send(content=f"Nombre d'images qui n'ont pas pu être affichées: {result['errors']}.", ephemeral=True)

# Fonction pour ajouter le cog
async def setup(bot):
    await bot.add_cog(Pybooru(bot))