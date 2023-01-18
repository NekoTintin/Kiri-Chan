import discord
from discord.ext import commands
import chat_exporter
from html2image import Html2Image

class Screenshot(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.command(name="screenshot", aliases=["Screenshot", "screen", "Screen"])
    async def screen(self, ctx, num: int=1):
        await ctx.message.delete()
        hist = await chat_exporter.export(
            ctx.channel,
            limit = num,
            bot = self.bot
        )
        message = await ctx.send("<a:search:944484192018903060> Création en cours...")
        if hist is None:
            return
        
        with open('hist.html', 'wb') as hist_file:
            hist_file.write(hist.encode())
        
        hti = Html2Image(output_path='/home/Tintin/discord_bot/Kiri-chan/')
        hti.screenshot(html_file='hist.html', save_as='screen.png')
        
        await message.delete()
        await ctx.send(file=discord.File("screen.png"))
        
        
async def setup(bot):
    await bot.add_cog(Screenshot(bot))