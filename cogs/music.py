# Bibliothèques de Discord
import discord
from discord.embeds import Embed
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# Autres
from validators import url as test_url
import yt_dlp as music
from tools.variables import sites_dict, online_message, ban_domain
import tools.formats as formats
import pyshorteners
from typing import Literal

# Pour le téléchargement
format_list = Literal["mp3", "ogg", "wav", "m4a"]

# Pour la lecture en streaming
ffmpeg_opts = {'options': '-vn'}
before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

# Options lister les vidéos d'une playlist
opts_playlist = {'extract_flat': 'in_playlist'}

# Options lister les informations d'une vidéo
opts_video = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]}

def get_video_list(search: str()) -> list() or None:
    video_list = list()
    with music.YoutubeDL(opts_playlist) as ytdl:
        if test_url(search): # Si search est une URL
            data = ytdl.extract_info(search, download=False)

            if data.get("extractor", None) in ban_domain:
                return None

            if data.get("_type", None) == "playlist":
                for num in range(data['playlist_count']):
                    video_list.append({
                        "video_url": data['entries'][num]['url'],
                        "video_title": data['entries'][num]['title'],
                        "video_index": num})
            else:
                video_list.append({"video_url": search,
                            "video_title": data['title'],
                            "video_index": 0})
        else:
            data = ytdl.extract_info(f"ytsearch:{search}", download=False)
            video_list.append({"video_url": data['entries'][0]['url'],
                            "video_title": data['entries'][0]['title'],
                            "video_index": 0})
    return video_list

def get_video_data(link: str()) -> dict():
    video_data = dict()
    with music.YoutubeDL(opts_video) as video:
        data = video.extract_info(link, download=False)
        video_data = {"id": data.get("id", None),
            "url": data.get("url", None),
            "channel_url": data.get("channel_url", None),
            "extractor": data.get("extractor", None),
            "thumbnail": data.get("thumbnail", None),
            "uploader": data.get("uploader", None),
            "duration": data.get("duration_string", None),
            "is_live": data.get("is_live", None)}
    return video_data

def time_convert(time) -> str():
    try:
        if len(time) == 2:
            return f"00:{time}"
        elif len(time) == 1:
            return f"00:0{time}"
    except:
        if time == None:
            return "Diffusion en direct"
    return time

def create_embed(data: dict(), title: str(), channel: str(), list_id: int(), list_max: int(), bot_name: str) -> Embed():
    list_id += 1

    emb = Embed(title=f"[{list_id}/{list_max}] **{title}**", description=f"***{bot_name}*** en cours de lecture dans 🔊 **{channel}**.",
                color=sites_dict[data["extractor"]]["color"])
    emb.set_image(url=data["thumbnail"])
    emb.set_footer(text=f"Depuis {data['extractor'].capitalize()} - ID: {data['id']} - Durée: {time_convert(data['duration'])}",
                   icon_url=sites_dict[data["extractor"]]["icon_url"])
    emb.set_author(name=f"{data['uploader']}", url=data["channel_url"])

    return emb

class Player():
    
    def __init__(self, bot: commands.Bot, voice: discord.VoiceClient, channel_name: str) -> None:
        # Variables pour le Bot
        self.bot = bot
        self.voice = voice
        self.channel_name = channel_name
        self.message_embed = None
        self.message_view = None
        # Variables pour la list
        self.list = list()
        self.name_list = list()
        self.list_id = int()
        self.list_max = int()
        # Variables pour la vidéo en cours de lecture
        self.video_data = dict()
        self.video_url = str()
        
    # Gestion de la lecture audio
    async def audio_play(self, playing_mode: bool = False) -> None:
        if self.voice.is_playing():
            await self.set_status(None)
            self.voice.stop()

        if playing_mode:
            self.video_data = get_video_data(self.list[self.list_id]['video_url'])
            self.video_url = self.video_data['url']
            self.message_embed = create_embed(self.video_data, self.list[self.list_id]['video_title'], self.channel_name, self.list_id, self.list_max, self.bot.user.display_name)
            self.message_view = await self.create_view(self.video_data['is_live'])
            await self.set_status(self.list[self.list_id]['video_title'])

            self.voice.play(discord.FFmpegOpusAudio(self.video_url, **ffmpeg_opts, before_options=before_options))
            
    # Change le statut du bot pendant la lecture
    async def set_status(self, title: str) -> None:
        if title == None:
            return await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))

    # Retourne une view avec les boutons de lecture
    async def create_view(self, is_live: bool) -> View:
        view = View(timeout=None)

        play_button = Button(label="Pause", style=discord.ButtonStyle.primary, emoji="⏸️", row=0)
        add_button = Button(label="Ajouter", style=discord.ButtonStyle.primary, emoji="➕", row=0)
        stop_button = Button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️", row=0)
        
        disc_button = Button(label="Déconnexion", style=discord.ButtonStyle.danger, emoji="❎", row=1)
        rewi_button = Button(label="Rembobiner", style=discord.ButtonStyle.primary, emoji="⏪", row=1)
        
        async def add_to_playlist(data) -> None:
            for video in data:
                self.list.append(video)
            self.list_max = len(self.list)

        async def change_embed() -> Embed and View:
            self.message_embed = create_embed(self.video_data, self.list[self.list_id]['video_title'], self.channel_name, self.list_id, self.list_max, self.bot.user.display_name)
            self.message_view = await self.create_view(self.video_data['is_live'])

            return self.message_embed, self.message_view

        # Fonctions des Boutons
        async def resume(react: discord.Interaction):
            await react.response.defer(thinking=False)
            if self.voice.is_playing() == True:
                self.voice.pause()
                play_button.label = "Reprendre"
                play_button.emoji = "▶️"
            else:
                self.voice.resume()
                play_button.label = "Pause"
                play_button.emoji = "⏸️"
            await react.message.edit(view=self.message_view)

        async def stop(react: discord.Interaction):
            await react.response.defer(thinking=False)
            await self.audio_play()
            await react.message.delete()
            
        async def add_music(react: discord.Interaction):
            class Add_Modal(discord.ui.Modal, title="Ajouter un lien ou une recherche."):
                link = discord.ui.TextInput(label="Entre ton lien ou ta recherche ici.",
                    style=discord.TextStyle.short,
                    placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    required=True)
    
                async def on_submit(self, react: discord.Interaction) -> None:
                    await react.response.defer(thinking=False, ephemeral=True)
                    await add_to_playlist(get_video_list(self.link.value))
                    await react.message.edit(suppress=True)

                    message_embed, message_view = await change_embed()
                    await react.message.edit(embed=message_embed, view=message_view)

            
            await react.response.send_modal(Add_Modal())
            
        async def disconnect(react: discord.Interaction):
            await react.response.defer(thinking=False)
            await self.audio_play()
            
            await self.voice.disconnect()
            await react.message.delete()
            self.voice = None
        
        async def rewind(react: discord.Interaction):
            await react.response.defer(thinking=False)
            await self.audio_play(playing_mode=True) 

        async def backward(react: discord.Interaction):
            await react.response.defer(thinking=False)
            self.list_id -= 1
            await self.audio_play(playing_mode=True)
            
            await react.message.edit(suppress=True)
            await react.message.edit(embed=self.message_embed, view=self.message_view)

        async def forward(react: discord.Interaction):
            await react.response.defer(thinking=False)
            self.list_id += 1
            await self.audio_play(playing_mode=True)
            
            await react.message.edit(suppress=True)
            await react.message.edit(embed=self.message_embed, view=self.message_view)
        
        #link_button = Button(label="Lien", style=discord.ButtonStyle.link, row=3, url=self.video_url)
        if not is_live:
            back_button = Button(label="Précédente", style=discord.ButtonStyle.primary, emoji="⏮️", row=2)
            forw_button = Button(label="Suivante", style=discord.ButtonStyle.primary, emoji="⏭️", row=2)

            short = pyshorteners.Shortener()
            short_url = short.tinyurl.short(self.video_url)
            down_button = Button(label="Télécharger", style=discord.ButtonStyle.link, url=short_url, row=3)

            back_button.callback = backward
            forw_button.callback = forward
            
            view.add_item(back_button)
            view.add_item(forw_button)
            view.add_item(down_button)

            current_vid = self.list_id + 1
            if self.list_max == 1:
                back_button.disabled = True
                forw_button.disabled = True
            elif current_vid == 1:
                back_button.disabled = True
            elif current_vid == self.list_max:
                forw_button.disabled = True
        
        play_button.callback = resume
        stop_button.callback = stop
        disc_button.callback = disconnect
        add_button.callback = add_music
        rewi_button.callback = rewind
        
        view.add_item(play_button)
        view.add_item(stop_button)
        view.add_item(disc_button)
        view.add_item(add_button)
        view.add_item(rewi_button)
        #view.add_item(link_button)

        return view
    
    async def play_sound(self, flux: str) -> dict():
        self.list = get_video_list(flux)
        if self.list == None:
            return {"content": "Ce site n'est pas supporté."}
        self.video_url = self.list[0]["video_url"]
        self.list_max = len(self.list)
                
        await self.audio_play(playing_mode=True)
        return {"embed": self.message_embed, "view": self.message_view}
        

@app_commands.guild_only()
class Music(commands.Cog, name="music"):
    
    def __init__(self, bot):
        self.bot = bot
        self.dict_of_player = dict()
        self.dict_of_message = dict()
        super().__init__()
        
    @app_commands.command(name="play", description="Joue le son d'une vidéo ou d'un live depuis un lien ou une recherche.")
    async def _play(self, react: discord.Interaction, flux: str):
        await self.bot.wait_until_ready()
        await react.response.defer(ephemeral=False)
        
        # Vérifie si l'utilisateur est connecté sans un salon vocal 
        try:
            channel = react.user.voice.channel
        except:
            return await react.followup.send("Connecte-toi à un salon vocal pour jouer de la musique.", ephemeral=True)
        
        guild = react.guild
        voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice == None:
            await channel.connect()
            voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        elif voice.is_playing() or voice.is_paused():
            return await react.followup.send("Kiri-chan est déjà connectée dans un autre salon.")
            
        if self.dict_of_player.get(guild.id, None) != None:
            self.dict_of_player[guild.id] = None
            current_player = Player(self.bot, voice, channel.name)
            self.dict_of_player[guild.id] = current_player
        else:
            current_player = Player(self.bot, voice, channel.name)
            self.dict_of_player[guild.id] = current_player
            
        message = await current_player.play_sound(flux)
        if message.get("content", None) != None:
            return await react.followup.send(content=message.get("content"), ephemeral=False)
        else:
            message = await react.followup.send(embed=message.get("embed"), view=message.get("view"), ephemeral=False)
            self.dict_of_message = {guild.id: message}
    
    @app_commands.command(name="disconnect", description="Déconnecte le bot.")
    async def _disconnect(self, react: discord.Interaction):
        guild = react.guild
        voice = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice == None:
            return await react.response.send_message("Je ne pas connectée à un salon vocal", ephemeral=True)
        await voice.disconnect()
        await react.response.send_message("Kiri-chan s'est déconnectée.", ephemeral=True)
        
    
    """@app_commands.command(name="playlist", description="Affiche la playlist en cours.")
    async def _playlist(self, react: discord.Interaction):
        guild = react.guild
        voice = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice == None:
            return await react.response.send_message("Je ne pas connectée à un salon vocal", ephemeral=True)
        
        await react.response.defer(thinking=False)
        current_player = self.dict_of_player[guild.id]
        list_of_music = await current_player.get_playlist()
        
    @app_commands.command(name="download", description="Télécharge depuis un lien vers convertis le fichier.")
    async def _download(self, react: discord.Interaction, flux: str, format: format_list):
        pass"""
    
async def setup(bot):
    await bot.add_cog(Music(bot))