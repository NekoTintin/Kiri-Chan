# Bibliothèques de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

# Autres
from praw import Reddit as Red
from random import randint
import tools.passwords as pwrd

# Défini l'objet Reddit pour accéder au compte de Kirlia-Chan
wrapper = Red(
    # ID pour s'identifier en tant que Bot sur Reddit
    client_id = pwrd.reddit_id,
    client_secret = pwrd.reddit_secret,
    user_agent = "discord.py:kirlia-chan-bot:v3.0(by u/tintin361yt)",
    # ID du compte Reddit
    username = "Kirlia-chan",
    password = pwrd.reddit_password,
    # Pour éviter les messages chiants d'Async PRAW
    check_for_async = False)

class Reddit(commands.GroupCog, name="reddit"):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
    
    # Retourne de dernier post d'un subreddit dans un message Embed
    @app_commands.command(name="last", description="Affiche le dernier post d'un Subreddit.")
    async def last(self, interaction: discord.Interaction, subreddit: str) -> None:
        await interaction.response.defer(ephemeral=False)
        msg_list = get_post(subreddit, "new", 1)
        if msg_list == None:
            return await interaction.response.send_message(content="Le Subreddit n'existe pas, vérifie que tu ne t'es pas trompé en écrivant la commande.", ephemeral=True)

        if msg_list["nsfw"] and interaction.channel.is_nsfw():
            return await interaction.followup.send("Le post contient du NSFW.")

        embed = Embed(title=msg_list["title"], description=msg_list["desc"], color=0xff4300)
        embed.set_author(name=msg_list["author"]["text"])
        embed.set_footer(text=msg_list["footer"]["text"], icon_url=msg_list["footer"]["img"])
        embed.set_image(url=msg_list["img"])

        await interaction.followup.send(embed=embed)
        

def get_post(sub: str, sort_type: str, limit: int) -> dict or None:
    # Vérifie si le subreddit existe sinon retourne un message d'erreur
    try:
        wrapper.subreddits.search_by_name(sub, exact=True)
    except:
        return None

    subreddit = wrapper.subreddit(sub)
    list_msg = dict()
    if sort_type == "new":
        for post in subreddit.new(limit=1):
            list_msg = {"title": f"Voici le dernier post sur r/**{sub.capitalize()}**",
            "desc": post.title, "nsfw": post.over_18, "url": post.url,
            "author": {
                "avatar": post.author.icon_img,
                "text": f"Post par u/{post.author}"},
            "footer": {
                "img": "https://www.redditinc.com/assets/images/site/reddit-logo.png",
                "text": f"Depuis Reddit - ID: {post.id}"}}
    else:
        for ite, post in subreddit.hot(limit=limit):
            if ite == randint(0, limit):
                list_msg = {"title": f"Voici le dernier post sur r/**{sub.capitalize()}**",
            "desc": post.title, "nsfw": post.over_18, "url": post.url,
            "author": {
                "avatar": post.author.icon_img,
                "text": f"Post par u/{post.author}"},
            "footer": {
                "img": "https://www.redditinc.com/assets/images/site/reddit-logo.png",
                "text": f"Depuis Reddit - ID: {post.id}"}}

    # Vérifie si le post contient une image ou un gif
    if list_msg["url"].startswith("https://i.redd.it/") or list_msg["url"].startswith("https://preview.redd.it"):
        list_msg["img"] = post.url
    return list_msg

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Reddit(bot))