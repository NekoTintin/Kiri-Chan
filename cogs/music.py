import discord
from discord.embeds import Embed
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, button, Select

from validators import url as test_url
import yt_dlp as music
from tools.variables import sites_dict, online_message, ban_domain, nekotintin_id
from data.custom_message import player_custom_message as cmessage
from tools.passwords import gapi
import pyshorteners
from googleapiclient.discovery import build
from random import randint as rd
from math import ceil
import asyncio
import re

# Pour la lecture en streaming
ffmpeg_opts = {'options': '-vn'}
before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'

# Options lister les vidéos d'une playlist
opts_playlist = {'extract_flat': 'in_playlist'}

# Options lister les informations d'une vidéo
opts_video = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'}]}

youtube = build("youtube", "v3", developerKey=gapi)

def get_video_list(search: str) -> list:
    video_list = list()
    try:
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
                            "extractor": data['extractor'],
                            "video_index": num})
                else:
                    video_list.append({"video_url": search,
                                "video_title": data['title'],
                                "extractor": data['extractor'],
                                "video_index": 0})
            else:
                data = ytdl.extract_info(f"ytsearch:{search}", download=False)
                video_list.append({"video_url": data['entries'][0]['url'],
                                "video_title": data['entries'][0]['title'],
                                "extractor": "youtube",
                                "video_index": 0})
        return video_list
    except:
        return None

def get_video_data(link: str) -> dict:
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

def time_convert(time) -> str:
    try:
        if len(time) == 2:
            return f"00:{time}"
        elif len(time) == 1:
            return f"00:0{time}"
        else:
            return time
    except:
        return None
    
def cut_title(number: str, title: str) -> str:
    title_size = 100 - len(number)
    return number + title[:title_size]

def create_embed(data: dict, title: str, next_title: str, voice_channel_id: int, list_id: int, list_max: int, video_link: str, next_link: str, user_id: int) -> Embed:
    list_id += 1
    extractor = sites_dict.get(data["extractor"], sites_dict["générique"])
    extractor["extractor"] = data["extractor"]
    if "cdn.discordapp.com" in video_link:
        extractor["extractor"] = "discord"
    if data["thumbnail"] != None:
        thumbnail = data["thumbnail"]
    else:
        thumbnail = sites_dict.get(extractor["extractor"], "générique")["thumbnail"]
    
    emb = Embed(title=f":headphones: **{title}**",
        description=f"Actuellement en cours de lecture dans <#{voice_channel_id}>.",
        color=sites_dict.get(extractor["extractor"])["color"],
        type="image",
        url=video_link)
    emb.set_image(url=thumbnail)
    
    if list_id == list_max:
        value_str = "**Fin de la Liste de lecture**"
    else:
        value_str = f"**{next_title}\n{next_link}**"
        
    if list_max > 1:
        emb.add_field(name=f"📋 Dans la Liste de lecture [{list_id}/{list_max}]",
            value=value_str,
            inline=False)
    
    if data["is_live"] == True or data["duration"] == None:
        emb.set_footer(icon_url=sites_dict.get(extractor["extractor"])["icon_url"], text=f"Streaming via {extractor['extractor'].capitalize()}")
    elif data["duration"] != None:
        emb.set_footer(icon_url=sites_dict.get(extractor["extractor"])["icon_url"], text=f"Streaming via {extractor['extractor'].capitalize()} | {time_convert(data['duration'])}")
    
    if data["extractor"] == "youtube":
        url = data["channel_url"].split("/channel/")[-1]
        response = youtube.channels().list(part="snippet", id=url).execute()
        avatar_url = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        emb.set_author(name=f"{data['uploader']}", url=data["channel_url"], icon_url=avatar_url)
    else:
        if not data["uploader"] == None:
            emb.set_author(name=f"{data['uploader']}", url=data["channel_url"])
    return emb

class Player():
    
    def __init__(self, bot: commands.Bot, voice: discord.VoiceClient, channel: discord.TextChannel, voice_channel: discord.VoiceChannel, user_id: int) -> None:
        # Variables pour le Bot
        self.bot = bot
        self.voice = voice
        self.channel = channel
        self.voice_channel = voice_channel
        self.message_embed = None
        self.message_view = None
        self.message_id = 0
        self.user_id = user_id
        # Variables pour la list
        self.list = []
        self.list_id = 0
        self.list_max = 0
        self.enable_random = False
        # Variables pour le SelectMenu
        self.current_in_selectoption = 0
        self.pagecur = 0
        self.page_max = 0
        self.page_dict = None
        self.select_list = None
        # Variables pour la vidéo en cours de lecture
        self.video_data = {}
        self.video_url = ""
        self.is_button = False
                
    # Gestion de la lecture audio
    async def audio_play(self, playing_mode: bool = False) -> None:
        if self.voice.is_playing():
            await self.set_status(None)
            self.voice.stop()

        if playing_mode:
            self.video_data = get_video_data(self.list[self.list_id]['video_url'])
            self.video_url = self.video_data['url']
            if self.list_id + 1 < len(self.list):
                next_title = self.list[self.list_id+1]['video_title']
                next_url = self.list[self.list_id+1]['video_url']
            else:
                next_title = None
                next_url = None
            self.message_embed = create_embed(self.video_data, self.list[self.list_id]['video_title'], next_title, self.voice_channel.id, self.list_id, self.list_max, self.list[self.list_id]["video_url"], next_url, self.user_id)
            self.message_view = await self.create_view(self.video_data['is_live'])
            await self.set_status(self.list[self.list_id]['video_title'])

            # Charge la prochaine musique dans le dict
            async def play_next():
                if self.is_button:
                    self.is_button = False
                    return None
                
                if not self.list_id + 1 == self.list_max:
                    if self.enable_random == True:
                        self.list_id = rd(0, self.list_max-1)
                    else:
                        self.list_id += 1
                    self.pagecur = int(self.list_id/20)
                    self.current_in_selectoption = self.list_id - self.pagecur*20
                    await self.audio_play(playing_mode=True)
                    message = await self.channel.fetch_message(self.message_id)
                    await message.edit(suppress=True)
                    await message.edit(embed=self.message_embed, view=self.message_view)
                    await asyncio.sleep(1)
                return None

            self.voice.play(discord.FFmpegPCMAudio(self.video_url, **ffmpeg_opts, before_options=before_options), after=lambda error: asyncio.run_coroutine_threadsafe(play_next(), self.bot.loop))

    # Change le statut du bot pendant la lecture
    async def set_status(self, title: str) -> None:
        if title == None:
            return await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))
        
    def _create_dict(self) -> dict:
        page_dict = {}
        page_limit = 20
        self.page_max = ceil(len(self.list)/page_limit)
        
        for num in range(self.page_max):
            page_dict[num] = self._create_select_list(self.list[num*page_limit:(num+1)*page_limit], num*page_limit, num)
        return page_dict
        
    def _create_select_list(self, video_list: list, start_num: int, cur_page: int) -> dict:
        select_list = []
        for num, link in enumerate(video_list):
            if num == self.current_in_selectoption:
                is_default = True
            else:
                is_default = False
            select_list.append(discord.SelectOption(label=cut_title(f"{start_num+num+1}. ", video_list[num]["video_title"]), description=video_list[num]["video_url"][:99], emoji=sites_dict.get(video_list[num]["extractor"], sites_dict["générique"])["emoji"], default=is_default))
        if cur_page > 0:
            select_list.append(discord.SelectOption(label=f"Page précédente", emoji="⬅️"))
        if cur_page < self.page_max - 1:
            select_list.append(discord.SelectOption(label=f"Page suivante", emoji="➡️"))
        return select_list
        

    # Retourne une view avec les boutons de lecture
    async def create_view(self, is_live: bool) -> View:
        view = View(timeout=None)
        
        self.page_dict = self._create_dict()
        self.select_list = self.page_dict[self.pagecur]

        if self.voice.is_playing() == False:
            play_button = Button(label="Pause", style=discord.ButtonStyle.success, emoji="<:pause_icon:1213236010071105596>", row=0)
        else:
            play_button = Button(label="Reprendre", style=discord.ButtonStyle.success, emoji="<:play_icon:1213235979708534866>", row=0)
        add_button = Button(label="Ajouter", style=discord.ButtonStyle.success, emoji="<:add_icon:1148310139900792923>", row=0)
        
        disc_button = Button(label="Déconnexion", style=discord.ButtonStyle.danger, emoji="<:disconnect_icon:1148310144703279134>", row=0)
        back_button = Button(label="Précédente", style=discord.ButtonStyle.primary, emoji="<:last_icon:1148310149690294294>", row=1)
        forw_button = Button(label="Suivante", style=discord.ButtonStyle.primary, emoji="<:forward_icon:1148310147265990750>", row=1)

        if self.enable_random == False:
            shuffle_button = Button(label="Shuffle", style=discord.ButtonStyle.green, emoji="<:shuffle_icon:1153724588103061595>", row=1)
        else:
            shuffle_button = Button(label="Activé", style=discord.ButtonStyle.green, emoji="<:shuffle_icon:1153724588103061595>", row=1)

        select_menu = Select(placeholder="Choisis une musique", max_values=1, min_values=1, options=self.select_list)
        
        async def add_to_playlist(data) -> None:
            for video in data:
                self.list.append(video)
            self.list_max = len(self.list)

        async def change_embed() -> Embed: # and View
            if self.list_id + 1 < len(self.list):
                next_title = self.list[self.list_id+1]['video_title']
                next_url = self.list[self.list_id+1]['video_url']
            else:
                next_title = None
                next_url = None
            self.message_embed = create_embed(self.video_data, self.list[self.list_id]['video_title'], next_title, self.voice_channel.id, self.list_id, self.list_max, self.list[self.list_id]["video_url"], next_url, self.user_id)
            self.message_view = await self.create_view(self.video_data['is_live'])

            return self.message_embed, self.message_view

        # Fonctions des Boutons
        async def resume(react: discord.Interaction):
            await react.response.defer(thinking=False)
            if self.voice.is_playing() == True:
                self.voice.pause()
                play_button.label = "Reprendre"
                play_button.emoji = "<:play_icon:1213235979708534866>"
            else:
                self.voice.resume()
                play_button.label = "Pause"
                play_button.emoji = "<:pause_icon:1213236010071105596>"
            await react.message.edit(view=self.message_view)
            
        async def add_music(react: discord.Interaction):
            class Add_Modal(discord.ui.Modal, title="Ajouter un lien ou une recherche"):
                link = discord.ui.TextInput(label="Entre ton lien ou ta recherche ici.",
                    style=discord.TextStyle.short,
                                            placeholder="https://www.youtube.com/watch?v=zuXdMjFCOow",
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
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))
    
        async def rewind(react: discord.Interaction):
            await react.response.defer(thinking=False)
            self.is_button = True
            await self.audio_play(playing_mode=True) 

        async def backward(react: discord.Interaction):
            await react.response.defer(thinking=False)
            self.list_id -= 1
            self.pagecur = int(self.list_id/20)
            self.is_button = True
            self.current_in_selectoption = self.list_id - self.pagecur*20

            await self.audio_play(playing_mode=True)
            await react.message.edit(suppress=True)
            await react.message.edit(embed=self.message_embed, view=self.message_view)

        async def forward(react: discord.Interaction):
            await react.response.defer(thinking=False)
            if self.enable_random == True:
                self.list_id = rd(0, self.list_max-1)
            else:
                self.list_id += 1

            self.pagecur = int(self.list_id/20)
            self.current_in_selectoption = self.list_id - self.pagecur*20
            self.is_button = True

            await self.audio_play(playing_mode=True)
            await react.message.edit(suppress=True)
            await react.message.edit(embed=self.message_embed, view=self.message_view)

        async def suffle(react: discord.Interaction):
            await react.response.defer(thinking=False)
            if self.enable_random == False:
                shuffle_button.label = "Activé"
                shuffle_button.emoji = "<:shuffle_icon:1153724588103061595>"
                self.enable_random = True
            else:
                shuffle_button.label = "Shuffle"
                shuffle_button.emoji = "<:shuffle_icon:1153724588103061595>"
                self.enable_random = False
            await react.message.edit(view=self.message_view)
            
        async def menu_callback(react: discord.Interaction):
            await react.response.defer(thinking=False)
            
            if select_menu.values[0] == "Page précédente":
                self.pagecur-=1
                self.current_in_selectoption = 0
                self.curall = self.pagecur*20
                
                self.message_view = await self.create_view(is_live)
                
                await react.message.edit(suppress=True)
                await react.message.edit(view=self.message_view)
                
            elif select_menu.values[0] == "Page suivante":
                self.pagecur+=1
                self.current_in_selectoption = 0
                self.curall = self.pagecur*20
                
                self.message_view = await self.create_view(is_live)
                
                await react.message.edit(suppress=True)
                await react.message.edit(view=self.message_view)
                
            else:
                self.current_in_selectoption = int((re.search(r'\d+', select_menu.values[0]).group()) if re.search(r'\d+', select_menu.values[0]) else None) - (self.pagecur*20) -1
                self.list_id = int((re.search(r'\d+', select_menu.values[0]).group()) if re.search(r'\d+', select_menu.values[0]) else None) -1
                
                if self.voice.is_playing():
                    self.voice.stop()
                self.is_button = True
                await self.audio_play(playing_mode=True)
            
                await react.message.edit(suppress=True)
                await react.message.edit(embed=self.message_embed, view=self.message_view)

        current_vid = self.list_id + 1
        if self.list_max == 1:
            back_button.disabled = True
            forw_button.disabled = True
            shuffle_button.disabled = True
        elif current_vid == 1:
            back_button.disabled = True
        elif current_vid == self.list_max:
            forw_button.disabled = True
        
        view.add_item(play_button)
        view.add_item(disc_button)
        view.add_item(add_button)

        if not is_live:
            rewi_button = Button(label="Rembobiner", style=discord.ButtonStyle.primary, emoji="<:back_icon:1148310142664851507>", row=1)

            short = pyshorteners.Shortener()
            short_url = short.isgd.short(self.video_url)
            down_button = Button(label="Télécharger", style=discord.ButtonStyle.link, url=short_url, row=0)

            view.add_item(down_button)
            view.add_item(rewi_button)
            rewi_button.callback = rewind
        
        play_button.callback = resume
        disc_button.callback = disconnect
        add_button.callback = add_music
        back_button.callback = backward
        forw_button.callback = forward
        shuffle_button.callback = suffle
        select_menu.callback = menu_callback
        
        view.add_item(back_button)
        view.add_item(forw_button)
        view.add_item(shuffle_button)
        view.add_item(select_menu)

        return view
    
    async def play_sound(self, flux: str) -> dict:
        self.list = get_video_list(flux)
        if self.list == None:
            return {"content": "Ce site n'est pas supporté."}
        self.video_url = self.list[0]["video_url"]
        self.list_max = len(self.list)
                
        await self.audio_play(playing_mode=True)
        return {"embed": self.message_embed, "view": self.message_view}
    
    def msg_id(self, id: int) -> int:
        if id == 0:
            return self.message_id
        self.message_id = id

@app_commands.guild_only()
class Music(commands.Cog, name="music"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.dict_of_player = dict()
        self.dict_of_message = dict()
        self.voice = None
        self.guild = None
        self.channel = None
        super().__init__()
        
    @app_commands.command(name="play", description="Joue le son d'une vidéo ou d'un live depuis un lien ou une recherche.")
    async def _play(self, react: discord.Interaction, flux: str, salon:str=None) -> None:
        await self.bot.wait_until_ready()
        await react.response.defer(ephemeral=False)
        
        self.guild = react.guild
        # Vérifie si l'utilisateur est connecté sans un salon vocal 
        try:
            voice_state = react.user.voice
            if voice_state is not None and voice_state.channel is not None:
                self.channel = voice_state.channel
            elif salon != None:
                self.channel = self.bot.get_channel(int(salon))
            else:
                return await react.followup.send("Connecte-toi à un salon vocal pour jouer de la musique.", ephemeral=True)
        except:
            return await react.followup.send("Connecte-toi à un salon vocal pour jouer de la musique.", ephemeral=True)
        
        self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=self.guild)    

        if self.voice == None:
            await self.channel.connect()
            self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=self.guild)
        elif self.voice != None:
            if self.dict_of_player.get(self.guild.id, None) != None:
                return await react.followup.send("Kiri-chan est déjà connectée. Pour lire une autre musique, ajoute la avec le bouton Ajouter. (c'est clairement une Skill Issue)")
        elif self.voice.is_playing() or self.voice.is_paused():
            return await react.followup.send("Kiri-chan est déjà connectée dans un autre salon. Pour lire une autre musique, ajoute la avec le bouton Ajouter.")
        
        try:
            if self.dict_of_player.get(self.guild.id, None) != None:
                self.dict_of_player[self.guild.id] = None
                current_player = Player(self.bot, self.voice, react.channel, self.channel, react.user.id)
                self.dict_of_player[self.guild.id] = current_player
            else:
                current_player = Player(self.bot, self.voice, react.channel, self.channel, react.user.id)
                self.dict_of_player[self.guild.id] = current_player
            
            message = await current_player.play_sound(flux)
            if message.get("content", None) != None:
                await react.followup.send(content=message.get("content"), ephemeral=False)
            else:
                sended_msg = await react.followup.send(embed=message.get("embed"), view=message.get("view"), ephemeral=False, wait=True)
                msg2 = await sended_msg.fetch()
                current_player.msg_id(msg2.id)
                self.dict_of_message = {self.guild.id: message}

            self.bot.loop.create_task(self._check_members_in_channel())
        except:
            await react.followup.send(f"Désolée, la fonction </play:1140307587120763011> est cassée mais tu peux te plaindre à {self.bot.get_user(nekotintin_id).mention} !")
    
    @app_commands.command(name="disconnect", description="Déconnecte le bot.")
    async def _disconnect(self, react: discord.Interaction):
        guild = react.guild
        voice = discord.utils.get(self.bot.voice_clients, guild=guild)
        if voice == None:
            return await react.response.send_message("Je ne pas connectée à un salon vocal", ephemeral=True)
        await voice.disconnect()
        await react.response.send_message("Kiri-chan s'est déconnectée.", ephemeral=True, delete_after=15)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))
            
    async def _check_members_in_channel(self):
        await self.bot.wait_until_ready()
        is_active = True

        while is_active:
            if len(self.channel.members) <= 1:
                is_active = False
                msg_id = self.dict_of_player[self.guild.id].msg_id(id=0)
                msg = await self.channel.fetch_message(msg_id)
                await msg.delete()
                
                await self.channel.guild.voice_client.disconnect()
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))
                
            await asyncio.sleep(600)

async def setup(bot):
    await bot.add_cog(Music(bot))
