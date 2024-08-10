from discord.ext import commands

import asyncio
import datetime as dt
from pytz import timezone

IST = timezone('Europe/Paris')

class Bdsm(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self._bdsm())
        
    async def _bdsm(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(969257662246182945)
        
        while not self.bot.is_closed():
            now = dt.datetime.now(IST)
            
            if now.hour == 12 and now.strftime('%A') == "Tuesday":
                await channel.send("https://culture-sympathique.fr/images/bdsmelvin.png")
                #await channel.send("Suite à l'augmentation du prix de l'API de Melvin, le BDSM et BDSMelvin s'arrête à partir d'aujourd'hui.")
                
            await asyncio.sleep(3600)
            
async def setup(bot):
    await bot.add_cog(Bdsm(bot))