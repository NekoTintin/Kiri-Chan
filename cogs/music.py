# Bibliothèques de Discord
import discord
from discord.embeds import Embed
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# Web Scrapping
from bs4 import BeautifulSoup
import json
import requests

# Autres
from validators import url as test_url
from requests import get
import yt_dlp as music
import re
import time
import secrets

save_path = "/var/www/html/youtube_audios/"
ffmpeg_opts = {'options': '-vn'}
before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

# Préférences pour le téléchargement en mp3
ytdl_mp3 = {'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}],
    'outtmpl':save_path + '%(id)s.%(ext)s'}

def get_video_data(search: str) -> dict():
    video_info = dict()
    with music.YoutubeDL(ytdl_mp3) as vid_data:
        if test_url(search): # Si search est une URL
            infos = vid_data.extract_info(search, download=False)
        else:
            infos = vid_data.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        
        video_info = {"title": infos.get("title", None),
                          "id": infos.get("id", None),
                          "url": infos.get("url", None)}
    return video_info

class Music_Player(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice = None
        self.current_url = None
        super().__init__()
        
    @app_commands.command(name="play", description="Joue une musique depuis un lien.")
    async def play(self, interaction: discord.Interaction, flux: str):
        await interaction.response.defer(ephemeral=False)
        
        data = get_video_data(flux)
        thumb = f"https://i3.ytimg.com/vi/{data['id']}/maxresdefault.jpg"
        
        try:
            channel = interaction.user.voice.channel
        except:
            await interaction.followup.send("Connecte-toi à un salon vocal pour jouer de la musique.")
            return
        
        color = discord.Color.from_str(f"#{secrets.token_hex(3)}")
        test_embed = Embed(title=data["title"], description=f"Lecture de la musique dans le salon vocal {channel.name}", color=color)
        test_embed.set_image(url=thumb)
        test_embed.set_footer(text=f"Depuis Youtube - ID: {data['id']}", icon_url="https://upload.wikimedia.org/wikipedia/commons/f/f4/Youtube-logo-red.png")
            
        guild = interaction.guild
        if self.voice == None:
            await channel.connect()
            self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
            
        self.current_url = data["url"]
        
        if self.voice.is_playing():
            self.voice.stop()
            
        self.voice.play(discord.FFmpegOpusAudio(data["url"], **ffmpeg_opts, before_options=before_options))
        
        
        # Buttons
        play_pause_button = Button(label="Pause", style=discord.ButtonStyle.primary, emoji="⏸️")
        rewind_button = Button(label="Rembobiner", style=discord.ButtonStyle.primary, emoji="⏮️")
        disconnect_button = Button(label="Déconnexion", style=discord.ButtonStyle.danger, emoji="❎")
        stop_button = Button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
        
        # View
        view = View(timeout=None)
        
        # Fonctions des Boutons
        async def resume(interaction: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.pause()
                play_pause_button.label = "Lecture"
                play_pause_button.emoji = "▶️"
            else:
                self.voice.resume()
                play_pause_button.label = "Pause"
                play_pause_button.emoji = "⏸️"
            await interaction.message.edit(view=view)
            await interaction.response.send_message("", delete_after=0.01, ephemeral=True)
            
        async def rewind(interaction: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
                
            if self.voice.is_paused():
                play_pause_button.label = "Pause"
                play_pause_button.emoji = "⏸️"
                await interaction.message.edit(view=view)
                
            self.voice.play(discord.FFmpegOpusAudio(data["url"], **ffmpeg_opts, before_options=before_options))
            await interaction.response.send_message("", delete_after=0.01, ephemeral=True)
            
        async def stop(interaction: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
            await interaction.message.delete()
            await interaction.response.send_message("", delete_after=0.01, ephemeral=True)
        
        async def disconnect(interaction: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
            await self.voice.disconnect()
            await interaction.message.delete()
            await interaction.response.send_message("", delete_after=0.01, ephemeral=True)
            
                        
        play_pause_button.callback = resume
        rewind_button.callback = rewind
        stop_button.callback = stop
        disconnect_button.callback = disconnect
        
        view.add_item(rewind_button)
        view.add_item(play_pause_button)
        view.add_item(stop_button)
        view.add_item(disconnect_button)
        
        await interaction.followup.send(embed=test_embed, view=view, ephemeral=False)
        
        
async def setup(bot):
    await bot.add_cog(Music_Player(bot))