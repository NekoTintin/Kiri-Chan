from dis import disco
import yt_dlp as yt
from validators import url as testUrl
from requests import get
import discord
from discord.ext import commands
from discord.embeds import Embed
from colorthief import ColorThief as thief
from tools import embed_generator as generator
import kiri
import time

save_path = "/var/www/html/youtube_audios/"

# Préférences pour le téléchargement en mp3
ytdl_mp3 = {'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}],
    'outtmpl':save_path + '%(id)s.%(ext)s'}

# Pareil pour le format ogg
ytdl_ogg = {'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'vorbis',
        'preferredquality': '192'}],
    'outtmpl':save_path + '%(id)s.%(ext)s'}

ffmpeg_opts = { 'options': '-vn' }


# Obtient les infos de la vidéo comme l'URL ou la miniature
def get_video_data(search: str) -> dict:
    video_info = dict()
    if testUrl(search): # Si search est une URL
        with yt.YoutubeDL(ytdl_mp3) as vid_data:
            infos = vid_data.extract_info(search, download=False)
            video_info = {"title": infos.get("title", None),
                      "id": infos.get("id", None),
                      "url": infos.get("url", None)}
    else:
        with yt.YoutubeDL(ytdl_mp3) as vid_data:
            infos = vid_data.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            video_info = {"title": infos.get("title", None),
                      "id": infos.get("id", None),
                      "url": infos.get("url", None)}
    
    return video_info


class FromYoutube(commands.Cog, name="Youtube module"):
    def __init__(self, bot, online_message):
        self.bot = bot
        self.voice = None
        self.current_url = None
        self.online_message = online_message  
        
    # Commandes pour le streaming depuis YouTube
    @commands.command(name="play")
    async def play(self, ctx, *content):
        await ctx.message.delete()
        # Transforme le tuple en query
        query = " ".join(content)
    
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche de la vidéo sur YouTube en cours...")
        data = get_video_data(query)
    
        thumb = "https://i.ytimg.com/vi_webp/" + data["id"] + "/maxresdefault.webp"
        with open("/home/Tintin/Desktop/Kiri-chan/images/youtube.png", "wb") as f:
            image = get(url=thumb)
            f.write(image.content)
           
        color_thief = thief("/home/Tintin/Desktop/Kiri-chan/images/youtube.png")
        col = color_thief.get_color(quality=9)
        color = discord.Colour.from_rgb(col[0], col[1], col[2])
        
        try:
            channel = ctx.message.author.voice.channel
        except:
            await ctx.send("Connecte-toi à un salon vocal pour jouer de la musique.")
            await search_msg.delete()
            return
        
        msg, image = generator.gen_embed_yt(
            {"title": data["title"],
            "description": f"Lecture de la vidéo dans le salon **{channel.name}**.",
            "image": {"name": "youtube.png", "path": "/home/Tintin/Desktop/Kiri-chan/images/"},
            "color": color})

        guild = ctx.guild
        self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        if self.voice == None:
            await channel.connect()
            self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        
        await search_msg.delete()
        self.current_url = data["url"]
        
        if self.voice.is_playing():
            self.voice.stop()
        
        self.voice.play(discord.FFmpegPCMAudio(data["url"], **ffmpeg_opts))
        await ctx.send(embed=msg, file=image)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=data["title"]))
        
        
    # Met en pause la musique
    @commands.command(name='pause', aliases=['p'])
    async def pause(self, ctx):
        await ctx.message.delete()
        try:
            await self.voice.pause()
        except:
            pass
        
        
    # Resume the music
    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete()
        try:
            await self.voice.resume()
        except:
            pass
        
        
    # Remet la musique à 00:00
    @commands.command(name="rewind", aliases=['restart'])
    async def retour_au_debut(self, ctx):
        await ctx.message.delete()
        try:
            if self.voice.is_playing():
                self.voice.stop()
            else:
                await ctx.send("Aucune musique n'est joue actuellement.")
                return
        except:
            await ctx.send("Aucune musique n'est joue actuellement.")
            return
        self.voice.play(discord.FFmpegPCMAudio(self.current_url, before_options="-ss 00:00:00.00"))

    
    # Arrête la musique qui est joué actuellement
    @commands.command(name='stop', aliases=['s'])
    async def stop(self, ctx):
        await ctx.message.delete()
        if self.voice.is_playing():
            self.voice.stop()
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=kiri.online_message))
        else:
            await ctx.send("Aucune musique n'est jouée actuellement")


    # Joue la musique de Dream dans un salon vocal
    @commands.command()
    async def dream(self, ctx):
        await ctx.message.delete()

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="la musique de Dream."))
        channel = ctx.message.author.voice.channel
        
        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        if self.voice == None:
            await voice.connect()
        else:
            await self.voice.move_to(channel)
            
        self.bot_voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if self.voice.is_playing():
                self.voice.stop()
        except:
            pass
        self.bot_voice.play(discord.FFmpegPCMAudio(f"{save_path}dream.mp3"))
            
    
    # Kiri-chan quit the voice channel
    @commands.command(name='disconnect', aliases=['leave', 'dis'])
    async def disconnect(self, ctx):
        await ctx.message.delete()
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.send("Je ne suis connectée dans aucun salon vocal.")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=self.online_message))
        
    
    # Play cheh sound in a voice channel
    @commands.command()
    async def cheh(self, ctx):
        await ctx.message.delete()
        
        channel = ctx.message.author.voice.channel
        
        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        if self.voice == None:
            await voice.connect()
        else:
            await self.voice.move_to(channel)
            
        self.bot_voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if self.bot_voice.is_playing():
                self.voice.stop()
        except:
            pass
        self.voice.play(discord.FFmpegPCMAudio(f"{save_path}cheh.mp3"))
        time.sleep(7)
        await ctx.voice_client.disconnect()
        
    # Aide pour les commandes Youtube
    @commands.command(name="helpYoutube", aliases=["helpyoutube", "helpYT"])
    async def aideYT(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_yt())
        
def get_help_yt():
  embedMsg = Embed(title="<:youtube:316620060221374466> Youtube", description="Liste des commandes pour Youtube", color=0xFF0000)
  #embedMsg.add_field(name="-ytdl [format] [recherche ou url]", value="Télécharge une vidéo Youtube (formats disponibles: MP3, OOG, MKV)")
  embedMsg.add_field(name="-play [recherche ou url]", value="Joue une musique depuis Youtube dans un salon vocal")
  embedMsg.add_field(name="-pause", value="Met en pause la musique")
  embedMsg.add_field(name="-stop", value="Arrête la musique en cours")
  embedMsg.add_field(name="-resume", value="Reprends la musique là où tu l'avais arrêtée")
  embedMsg.add_field(name="-cheh", value="Quand le karma est contre toi...")
  embedMsg.add_field(name="-dream", value="Joue la musique de Dream dans un salon vocal")
  embedMsg.add_field(name="-disconnect", value="Je quitte le salon vocal")

  return embedMsg
        
def setup(bot):
    bot.add_cog(FromYoutube(bot, kiri.online_message))