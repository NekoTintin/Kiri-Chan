# Bibliothèques de Discord
import discord
from discord.embeds import Embed
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# Autres
from validators import url as test_url
import yt_dlp as music
from tools.variables import sites_dict
import secrets

ffmpeg_opts = {'options': '-vn'}
before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

# Préférences pour le téléchargement en mp3
ytdl_mp3 = {'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}],
    'outtmpl':'/home/Tintin' + '%(id)s.%(ext)s'}

def get_video_data(search: str) -> dict():
    video_info = dict()
    with music.YoutubeDL(ytdl_mp3) as vid_data:
        if test_url(search): # Si search est une URL
            infos = vid_data.extract_info(search, download=False)
        else:
            infos = vid_data.extract_info(f"ytsearch:{search}", download=False)['entries'][0]

        video_info = {"title": infos.get("title", None),
                            "id": infos.get("id", None),
                            "url": infos.get("url", None),
                            "site": infos.get("webpage_url_domain", None),
                            "is_live_stream": infos.get("is_live")}
        return video_info
        

class Music_Player(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice = None
        self.current_url = None
        self.current_site = None
        self.is_live_stream = False
        super().__init__()
        
    @app_commands.command(name="play", description="Joue le son d'une vidéo ou d'un live depuis un lien.")
    async def play(self, react: discord.Interaction, flux: str):
        await react.response.defer(ephemeral=False)
        
        data = get_video_data(flux)
        self.current_url = data['url']
        self.current_site = data["site"]
        self.is_live_stream = data["is_live_stream"]
        if self.current_site == "twitch.tv":
            self.current_site = "twitch.com"

        if self.current_site == "deezer.com":
            await react.followup.send("Deezer gratuit ne permet la lecture que des 30 premières secondes de la musique.", ephemeral=True)
        elif self.current_site == "spotify.com" or self.current_site == "music.apple.com":
            await react.followup.send("Ce site n'est pas supporté.", ephemeral=True)
        
        if self.current_site in sites_dict:
            thumbnail = sites_dict[self.current_site]["thumbnail_url"].replace("vid_id", data['id'])
            footer_text = f"Depuis {self.current_site[:-4].capitalize()} - ID: {data['id']}"
            footer_url = sites_dict[self.current_site]["icon_url"]
            color = sites_dict[self.current_site]["color"]
        else:
            thumbnail = "https://images.frandroid.com/wp-content/uploads/2018/08/guide-apps-video-android.jpg"
            footer_text = "Source inconnue"
            footer_url = "https://images.generation-msx.nl/company/0388910c.png"
            color = discord.Color.from_str(f"#{secrets.token_hex(3)}")
        
        try:
            channel = react.user.voice.channel
        except:
            await react.followup.send("Connecte-toi à un salon vocal pour jouer de la musique.", ephemeral=True)
            return
        
        test_embed = Embed(title=data["title"], description=f"Lecture de la musique dans le salon vocal **{channel.name}**", color=color)
        test_embed.set_image(url=thumbnail)
        test_embed.set_footer(text=footer_text, icon_url=footer_url)
            
        guild = react.guild
        if self.voice == None:
            await channel.connect()
            self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        
        
        if self.voice.is_playing():
            self.voice.stop()
            
        self.voice.play(discord.FFmpegOpusAudio(self.current_url, **ffmpeg_opts, before_options=before_options))
        
        
        # Buttons
        play_pause_button = Button(label="Pause", style=discord.ButtonStyle.primary, emoji="⏸️")
        rewind_button = Button(label="Rembobiner", style=discord.ButtonStyle.primary, emoji="⏮️")
        disconnect_button = Button(label="Déconnexion", style=discord.ButtonStyle.danger, emoji="❎")
        stop_button = Button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
        
        # View
        view = View(timeout=None)
        
        # Fonctions des Boutons
        async def resume(react: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.pause()
                play_pause_button.label = "Lecture"
                play_pause_button.emoji = "▶️"
            else:
                self.voice.resume()
                play_pause_button.label = "Pause"
                play_pause_button.emoji = "⏸️"
            await react.message.edit(view=view)
            await react.response.send_message("", delete_after=0.01, ephemeral=True)
            
        async def rewind(react: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
                
            if self.voice.is_paused():
                play_pause_button.label = "Pause"
                play_pause_button.emoji = "⏸️"
                await react.message.edit(view=view)
                
            self.voice.play(discord.FFmpegOpusAudio(data["url"], **ffmpeg_opts, before_options=before_options))
            await react.response.send_message("", delete_after=0.01, ephemeral=True)
            
        async def stop(react: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
            await react.message.delete()
            await react.response.send_message("", delete_after=0.01, ephemeral=True)
        
        async def disconnect(react: discord.Interaction):
            if self.voice.is_playing() == True:
                self.voice.stop()
            await self.voice.disconnect()
            self.voice = None
            await react.message.delete()
            await react.response.send_message("", delete_after=0.01, ephemeral=True)
            
                        
        play_pause_button.callback = resume
        rewind_button.callback = rewind
        stop_button.callback = stop
        disconnect_button.callback = disconnect
        
        if self.is_live_stream == False:
            view.add_item(rewind_button)
        view.add_item(play_pause_button)
        view.add_item(stop_button)
        view.add_item(disconnect_button)
        
        await react.followup.send(embed=test_embed, view=view, ephemeral=False)
        
        
async def setup(bot):
    await bot.add_cog(Music_Player(bot))