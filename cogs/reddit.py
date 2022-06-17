# -- coding: utf-8 --
# Importation de bibliothèques
from discord.ext import commands
from discord.embeds import Embed
from praw import Reddit as praw2zeretour
from random import randint
from discord import Colour
from requests import get
from colorthief import ColorThief as thief
# Autres fichiers du répertoires
import tools.passwords as pwrd
import tools.embed_generator as generator

# Défini l'objet Reddit pour accéder au compte de Kirlia-Chan
reddit = praw2zeretour(
    # ID pour s'identifier en tant que Bot sur Reddit
    client_id = pwrd.reddit_id,
    client_secret = pwrd.reddit_secret,
    user_agent = "discord.py:kirlia-chan-bot:v2.0.0(by u/tintin361yt)",
    # ID du compte Reddit
    username = "Kirlia-chan",
    password = pwrd.reddit_password,
    # Pour éviter les messages chiants d'Async PRAW
    check_for_async = False)

class FromReddit(commands.Cog, name="Reddit module"):
    # Initialisation
    def __init__(self, bot):
        self.bot = bot

    # Envoie le dernier post d'un subreddit dans un message Embed
    @commands.command(name="last")
    async def last(self, ctx, sub):
        await ctx.message.delete()
        # Petit message d'attente
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche sur Reddit en cours...")
        
        liste = get_post(sub, "new", None)
        submission, image = generator.gen_embed_reddit(liste)
    
        # Envoie le message en MP si le post est NSFW et que le salon ne l'est pas
        if liste["nsfw"] == True and ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW (Je t'ai envoyé l'URL en privé).")
            if liste["image"] != None:
                return await ctx.send(file=image, embed=submission)
            return await ctx.send(embed=submission)
    
        # Permet de vérifier si le post contient une image
        if liste["image"] != None:
            return await ctx.send(file=image, embed=submission)
        await search_msg.delete()
        await ctx.send(embed=submission)
        
    
    # Envoie un post d'un subreddit dans un message Embed
    @commands.command(name="hot")
    async def hot(self, ctx, sub):
        await ctx.message.delete()
        # Petit message d'attente
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche sur Reddit en cours...")
    
        liste = get_post(sub, "hot", 30)
        submission, image = generator.gen_embed_reddit(liste)
    
        # Envoie le message en MP si le post est NSFW et que le salon ne l'est pas
        if liste["nsfw"] == True and ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW (Je t'ai envoyé l'URL en privé).")
            if liste["image"] != None:
                return await ctx.send(file=image, embed=submission)
            return await ctx.send(embed=submission)
    
        if liste["image"] != None:
            return await ctx.send(file=image, embed=submission)
        await ctx.send(embed=submission)
        await search_msg.delete()
        
    
    # Envoie un post du subreddit r/Wallpaper
    @commands.command(name="wallpaper", aliases=["Wallpaper"])
    async def wall(self, ctx):
        await ctx.message.delete()
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche sur Reddit en cours...")
        liste = get_post("wallpaper", "hot", 30)
        submission, image = generator.gen_embed_reddit(liste)
        await search_msg.delete()
        await ctx.send(file=image, embed=submission)
        
        
    # Envoie un post du subreddit r/CrappyDesign
    @commands.command(name="crappy", aliases=["Crappy"])
    async def crappy(self, ctx):
        await ctx.message.delete()
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche sur Reddit en cours...")
        liste = get_post("crappydesign", "hot", 30)
        submission, image = generator.gen_embed_reddit(liste)
        await search_msg.delete()
        await ctx.send(file=image, embed=submission)
        
        
    # Envoie un post d'un subreddit dans un message Embed
    @commands.command(name="honkai")
    async def honkai(self, ctx):
        await ctx.message.delete()
        # Petit message d'attente
        search_msg = await ctx.send("<a:search:944484192018903060> Recherche sur Reddit en cours...")
    
        liste = get_post("houkai3rd", "hot", 30)
        submission, image = generator.gen_embed_reddit(liste)
    
        # Envoie le message en MP si le post est NSFW et que le salon ne l'est pas
        if liste["nsfw"] == True and ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW (Je t'ai envoyé l'URL en privé).")
            if liste["image"] != None:
                return await ctx.send(file=image, embed=submission)
            return await ctx.send(embed=submission)
    
        if liste["image"] != None:
            return await ctx.send(file=image, embed=submission)
        await ctx.send(embed=submission)
        await search_msg.delete()
        
        
    # Upvote un post Reddit
    @commands.command(name="upvote", aliases=["up"])
    async def up(self, ctx, post):
        await ctx.message.delete()
        result = upvote(post)
        if result == None:
            return await ctx.send("<:Erreur:945123023546093611> Impossible de récupérer les données du post.")
        await ctx.send(f"Le post a bien été upvoté ! (Score : **{get_score(post)}**)")
        
        
    # Envoie le score d'un post Reddit
    @commands.command(name="score")
    async def score(self, ctx, post):
        await ctx.message.delete()
        score = get_score(post)
        if score == None:
            return await ctx.send("<:Erreur:945123023546093611> Je n'arrive pas à récupérer le score du post.")
        await ctx.send(f"Le score du post est de **{score}**")
        
        
    # Envoie les commentaires d'un post
    @commands.command(name="comments", aliases=["com"])
    async def com(seld, ctx, id):
        await ctx.message.delete()
        comments = get_comments(id)
        if comments == False:
            await ctx.send("Ce post ne possède aucun commentaires.")
            return
        await ctx.send(embed=comments)
        
    
    # Aide pour les commandes Reddit
    @commands.command(name="helpReddit", aliases=["helpreddit"])
    async def aideRed(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=get_help_reddit())
    

def get_post(sub: str, sort: str, limit: int) -> dict:
    subreddit = reddit.subreddit(sub)
    liste_message = {}
    
    # Vérifie si le subreddit existe sinon retourne un message d'erreur
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except:
        error_liste = {"title": "<:Erreur:945123023546093611> Subreddit inexistant",
                       "description": "Le subreddit n'existe pas, vérifie que tu ne t'es pas trompé dans le nom.",
                       "color": 0xff4300, "image": None, "nsfw": False, "url": None, "id": None}
        return error_liste
    
    
    # Obtient tous les post du subreddit en les triant par new ou hot
    if sort == "new":
        for submission in subreddit.new(limit=1):
            # Stocke les informations dans liste_message
            liste_message = {"title": f"Voici le dernier post sur r/{sub} par u/{submission.author}:",
                       "description": submission.title,
                       "color": 0xff4300, "image": None, "nsfw": submission.over_18, "url": submission.url, "id": submission.id}        
    else:
        stop_num = randint(0, limit)
        for iteration, submission in enumerate(subreddit.hot(limit=limit)):
            if stop_num == iteration:
                # Stocke les informations dans liste_message
                liste_message = {"title": f"Voici un post sur r/{sub} par u/{submission.author}:",
                       "description": submission.title,
                       "color": 0xff4300, "image": None, "nsfw": submission.over_18, "url": submission.url, "id": submission.id}
                            
    
    # Enregistre l'image du post, s'il y en a une
    if liste_message["url"].startswith("https://i.redd.it/"):
        with open("/home/Tintin/Desktop/Kiri-chan/images/reddit.png", "wb") as f:
            image = get(url=liste_message["url"])
            f.write(image.content)
        liste_message["image"] = {"name": "reddit.png", "path": "/home/Tintin/Desktop/Kiri-chan/images/"}
            
        # Obtient la color dominante de l'image
        color_thief = thief("/home/Tintin/Desktop/Kiri-chan/images/reddit.png")
        temp = color_thief.get_color(quality=9)
        
        # La convertie en couleur pour Discord
        color = Colour.from_rgb(temp[0], temp[1], temp[2])
        liste_message["color"] = color
        
    return liste_message

# Permet d'upvote le post avec l'ID
def upvote(post):
    sub = reddit.submission(post)
    try:
        sub.upvote()
    except:
        return None
    return get_score(post)

# Permet d'obtenir le score d'un post
def get_score(post):
    sub = reddit.submission(post)
    try:
        score = sub.score
    except:
        return None
    return score

def get_comments(id):
  post = reddit.submission(id=id)
  post.comment_sort = "new"
  top_com = list(post.comments)
  
  long_top_com = len(top_com)
  if long_top_com == 0:
    return None
  elif long_top_com < 6:
    leng = long_top_com
  else:
    leng = 6
  
  message = Embed(title="Commentaires les plus récents:", description="", color=0xff4300)
  for i in range (0, leng):
    p = top_com[i]
    message.add_field(name=f"Commentaire de :{p.author}", value=f"{p.body}", inline=False)
    
  return message

def get_help_reddit():
  embedMsg = Embed(title="<:reddit:794069835138596886> Reddit", description="Liste des commandes pour Reddit", color=0xff4300)
  embedMsg.add_field(name="-last [nom du subreddit]", value="Obtiens le dernier post d'un subreddit")
  embedMsg.add_field(name="-hot [nom du subreddit]", value="Obtiens un post populaire au hasard d'un subreddit")
  embedMsg.add_field(name="-wallpaper", value="Retourne un post du subreddit r/Wallpaper")
  embedMsg.add_field(name="-honkai", value="Affiche un post du subreddit r/Houkai3rd")
  embedMsg.add_field(name="-crappy", value="Affiche un post du subreddit r/CrappyDesign")
  embedMsg.add_field(name="-upvote [ID ou URL]", value="Upvote le dernier post que j'affiche")
  embedMsg.add_field(name="-score [ID ou URL]", value="Affiche le score du post")
  embedMsg.add_field(name="-comments", value="Affiche les commentaires d'un post.")

  return embedMsg

def setup(bot):
    bot.add_cog(FromReddit(bot))