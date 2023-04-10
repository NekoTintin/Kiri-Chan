from discord.ext import commands

import asyncio
import datetime as dt
from pytz import timezone

IST = timezone('Europe/Paris')

class Bdsm(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self._bdsm())
        bot.loop.create_task(self._annoying_ping())
        
    async def _bdsm(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(969257662246182945)
        
        while not self.bot.is_closed():
            now = dt.datetime.now(IST)
            
            if now.hour == 12 and now.strftime('%A') == "Tuesday":
                await channel.send("https://media.discordapp.net/attachments/969257662246182945/1062388761947803708/unknown-7-1-1.png?width=960&height=480")
                
            await asyncio.sleep(3600)
    
    async def _annoying_ping(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(830093950111055933)
        while not self.bot.is_closed():
            now = dt.datetime.now(IST)
            marie = self.bot.get_user(682217361092378671)
            
            if now.hour == 3:
                await channel.send(content=f"{marie.mention}")
                
            await asyncio.sleep(3600)
    
async def setup(bot):
    await bot.add_cog(Bdsm(bot))