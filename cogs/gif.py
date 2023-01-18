from discord.ext import commands
  
class Gif(commands.Cog):
    # Fonction d'initialisation
    def __init__(self, bot) -> None:
        self.bot = bot
        
    
        
async def setup(bot):
    await bot.add_cog(Gif(bot))
