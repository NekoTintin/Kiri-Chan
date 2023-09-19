# Biblio de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

from googlesearch import search
from urllib.parse import urlparse

# Module du bot
import tools.variables as var

class Search(commands.GroupCog, name="search"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="google", description="Fait un recherche sur Google.")
    async def _google(self, react: discord.Interaction, query: str) -> None:
        await self.bot.wait_until_ready()
        await react.response.defer()
        
        results = search(term=query, num_results=10, lang="fr")
        
        emb = Embed(title=f"Recherche sur Google: {query}", color=0x4285f4)
        emb.set_footer(icon_url="https://cdn-icons-png.flaticon.com/512/2875/2875331.png", text="Depuis Google.fr")
        for res in results:
            url = urlparse(res)
            site_name = url.netloc
            emb.add_field(name=site_name, value=res, inline=False)
        await react.followup.send(embed=emb)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Search(bot))