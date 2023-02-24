import discord
from discord.ext import commands
from discord import app_commands

import chat_exporter
from html2image import Html2Image

class Screenshot(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
        
    @app_commands.command(name="screenshot", description="desc")
    async def screen(self, interaction: discord.Interaction, nombre: int=1):
        if nombre <= 0:
            await interaction.response.send_message("Le nombre de message doit être supérieur à 0.", ephemeral=True)
        
        await interaction.response.defer(ephemeral=False)
        msg_hist = await chat_exporter.export(interaction.channel, limit=nombre, bot=self.bot)
        
        
        
    """
    @commands.command(name="screenshot", aliases=["Screenshot", "screen", "Screen"])
    async def screen(self, ctx, num: int=1):
        await ctx.message.delete()
        hist = await chat_exporter.export(
            ctx.channel,
            limit = num,
            bot = self.bot)
        message = await ctx.send("<a:search:944484192018903060> Création en cours...")
        if hist is None:
            return
        
        with open('hist.html', 'wb') as hist_file:
            hist_file.write(hist.encode())
        
        hti = Html2Image(output_path='/home/Tintin/discord_bot/Kiri-chan/')
        hti.screenshot(html_file='hist.html', save_as='screen.png')
        
        await message.delete()
        await ctx.send(file=discord.File("screen.png"))
    """
        
        
async def setup(bot):
    await bot.add_cog(Screenshot(bot))