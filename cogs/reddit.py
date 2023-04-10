# Bibliothèques de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

# Autres
from datetime import datetime
from praw import Reddit as Red
from secrets import SystemRandom
import tools.passwords as pwrd

# Défini l'objet Reddit pour accéder au compte de Kirlia-Chan
wrapper = Red(
    # ID pour s'identifier en tant que Bot sur Reddit
    client_id = pwrd.reddit_id,
    client_secret = pwrd.reddit_secret,
    user_agent = "discord.py:kirlia-chan-bot:v3.1.0(by u/tintin361yt)",
    # ID du compte Reddit
    username = "Kirlia-chan",
    password = pwrd.reddit_password,
    # Pour éviter les messages chiants d'Async PRAW
    check_for_async = False)

def vote(id: str, is_upvote: bool = True) -> str:
    sub = wrapper.submission(id)
    try:
        if is_upvote:
            sub.upvote()
        else:
            sub.downvote()
    except:
        None
    return get_score(id)

def get_score(id: str) -> str:
    sub = wrapper.submission(id)
    try:
        score = sub.score
    except:
        return None
    return score

class Posts_Button(discord.ui.View):

    def __init__(self, *, timeout = None):
        self.is_upvoted = False
        self.is_downvoted = False
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="Ajouter à ta liste", style=discord.ButtonStyle.success, emoji="📝", disabled=True)
    async def _add_to_list(self, react: discord.Interaction, button: discord.ui.Button):
        id = react.user.id
        link = react.message.embeds[0].image.url
        
        try:
            with open(f"/home/Tintin/discord_bot/NekoBot/data/{id}.txt", "a") as file:
                file.write(f"{link}\n")
            await react.response.send_message("✅ Ajouté à ta liste !", delete_after=15, ephemeral=True)
            return
        except:
            await react.response.send_message("❌ Impossible de l'ajouter à la liste...", delete_after=15, ephemeral=True)
            return
        
    @discord.ui.button(label=f"Upvote", style=discord.ButtonStyle.primary, emoji="🔼", row=1)
    async def _upvote(self, react: discord.Interaction, button: discord.ui.Button):
        await react.response.defer(thinking=False)
        if self.is_upvoted:
            return await react.followup.send("❌ Tu a déjà upvoté ce post !", ephemeral=True)
        elif self.is_downvoted:
            return await react.followup.send("❌ Tu a déjà downvoté ce post !", ephemeral=True)
        
        score = vote(react.message.embeds[0].footer.text[-7:], True)
        button.label = f"Upvoté ({score})"
        self.is_upvoted = True
        await react.message.edit(view=self)
        
    @discord.ui.button(label="Downvote", style=discord.ButtonStyle.danger, emoji="🔽", row=1)
    async def _downvote(self, react: discord.Interaction, button: discord.ui.Button):
        await react.response.defer(thinking=False)
        if self.is_upvoted:
            return await react.followup.send("❌ Tu a déjà upvoté ce post !", ephemeral=True)
        elif self.is_downvoted:
            return await react.followup.send("❌ Tu a déjà downvoté ce post !", ephemeral=True)
        
        score = vote(react.message.embeds[0].footer.text[-7:], False)
        button.label = f"Downvoté ({score})"
        self.is_downvoted = True
        await react.message.edit(view=self)
    

class Reddit(commands.GroupCog, name="reddit"):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
    # Retourne de dernier post d'un subreddit dans un message Embed
    @app_commands.guild_only()
    @app_commands.command(name="last", description="Affiche le dernier post d'un Subreddit.")
    async def _last(self, react: discord.Interaction, subreddit: str) -> None:
        await react.response.defer(ephemeral=False)
        content = get_post(subreddit, "new", 1, react.channel.is_nsfw())
        
        if content == None:
            return await react.followup.send(content="Le Subreddit n'a pas été trouvé, vérifie que tu ne t'es pas trompé en écrivant la commande.", ephemeral=True)
        elif content.get("nsfw") == True:
            return await react.followup.send("Ce post contient du NSFW, utilise la commande dans un salon NSFW.", ephemeral=True)

        await react.followup.send(embed=content.get("message"), view=content.get("view"), ephemeral=False)
        
        
    # Retourne un post parmi les x premier de hot
    @app_commands.guild_only()
    @app_commands.command(name="hot", description="Affiche un post populaire au hasard d'un subreddit.")
    async def _hot(self, react: discord.Interaction, subreddit: str) -> None:
        await react.response.defer(ephemeral=False)
        content = get_post(subreddit, "hot", 30, react.channel.is_nsfw())
        
        if content == None:
            return await react.followup.send(content="Le Subreddit n'a pas été trouvé, vérifie que tu ne t'es pas trompé en écrivant la commande.", ephemeral=True)
        elif content.get("nsfw") == True:
            return await react.followup.send("Ce post contient du NSFW, utilise la commande dans un salon NSFW.", ephemeral=True)

        await react.followup.send(embed=content.get("message"), view=content.get("view"), ephemeral=False)
        
        
    @app_commands.guild_only()
    @app_commands.command(name="wallpaper", description="Affiche un post du subreddit r/Wallpaper.")
    async def _wallpaper(self, react: discord.Interaction) -> None:
        await react.response.defer(ephemeral=False)
        content = get_post("wallpaper", "hot", 30, react.channel.is_nsfw())
        await react.followup.send(embed=content.get("message"), view=content.get("view"), ephemeral=False)
        
        
    @app_commands.guild_only()
    @app_commands.command(name="crappydesign", description="Affiche un post du subreddit r/CrappyDesign.")
    async def _crappy(self, react: discord.Interaction) -> None:
        await react.response.defer(ephemeral=False)
        content = get_post("crappydesign", "hot", 30, react.channel.is_nsfw())
        await react.followup.send(embed=content.get("message"), view=content.get("view"), ephemeral=False)
        
        
    @app_commands.guild_only()
    @app_commands.command(name="honkai", description="Affiche un post du subreddit r/HonkaiImpact3rd.")
    async def _honkai(self, react: discord.Interaction) -> None:
        await react.response.defer(ephemeral=False)
        content = get_post("HonkaiImpact3rd", "hot", 30, react.channel.is_nsfw())
        await react.followup.send(embed=content.get("message"), view=content.get("view"), ephemeral=False)
        
        
    @app_commands.command(name="score", description="Affiche le score d'un post reddit.")
    async def _score(self, react: discord.Interaction, post_id: str) -> None:
        await react.response.defer(ephemeral=True)
        content = get_score(post_id)
        await react.followup.send(content=f"Le score de ce post est de **{content}**.", ephemeral=True)
        

def get_post(sub: str, sort_type: str, limit: int, is_nsfw: bool) -> dict or None:
    # Vérifie si le subreddit existe sinon retourne un message d'erreur
    if wrapper.subreddits.search_by_name(query=sub, exact=True) == None:
        return None

    post = None
    message = Embed
    if sort_type == "new":
        for p in wrapper.subreddit(sub).new(limit=1):
            post = p
        message = Embed(title=f"Voici le dernier post sur r/**{sub.capitalize()}**", description=post.title, color=0xFF5700)
    elif sort_type == "hot":
        num = SystemRandom().randint(0, limit)
        for i, p in enumerate(wrapper.subreddit(sub).hot(limit=limit)):
            if i == num:
                post = p
                break
        message = Embed(title=f"Voici un post sur r/**{sub.capitalize()}**", description=post.title, color=0xFF5700)

    if post.over_18 != is_nsfw:
        return {"nsfw": True}
    
    if post.selftext != "":
        if len(post.selftext) > 1024:
            message.add_field(name="Contenu", value=f"{post.selftext[:1021]}...")
        else:
            message.add_field(name="Contenu", value=post.selftext)
        
    message.set_author(name=f"u/{post.author.name}", icon_url=post.author.icon_img)
    message.set_footer(text=f"Posté le {timestamp_to_human(post.created_utc)} sur Reddit - ID: {post.id}", icon_url="https://www.redditinc.com/assets/images/site/reddit-logo.png")
    message.set_thumbnail(url=wrapper.subreddit(sub).icon_img)

    view = Posts_Button()
    view.add_item(discord.ui.Button(label="Lien vers le post", style=discord.ButtonStyle.link, url=post.url))

    # Vérifie si le post contient une image ou un gif
    if post.url.startswith("https://i.redd.it") or post.url.startswith("https://preview.redd.it") or post.url.startswith("https://i.imgur.com"):
        message.set_image(url=post.url)
        view.children[0].disabled = False
    
    return {"message": message, "view": view}

def timestamp_to_human(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y à %H:%M:%S")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Reddit(bot))