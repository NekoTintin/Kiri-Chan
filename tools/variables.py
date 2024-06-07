from typing import Literal

ver_num = "3.7.2"
online_message = "しかのこのこのここしたんたん"

mods = {}
nekotintin_id = 443113150599004161

def enable_module(mod):
    mods[mod] = "✅"
    
def disable_module(mod):
    mods[mod] = "❌"
    
def get_modules():
    return mods

keywords = ["général", "meme", "accueil", "seal-zone", "bienvenue"]
    
ban_domain = ["twitter", "deezer", "spotify"]

values = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]
    
sites_dict = {
    "dailymotion": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/dailymotion.png",
        "emoji": "<:dailymotion:1213230598597124127>",
        "color": 0x00bff9,
        "message": None
    },
    "soundcloud": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/soundcloud.png",
        "emoji": "<:soundcloud:1213230602787225743>",
        "color": 0xff6800,
        "message": None
    },
    "tiktok": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/tiktok.png",
        "emoji": "<:tiktok:1213230604309758023>",
        "color": 0xee1d52,
        "message": None
    },
    "twitch": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/twitch.png",
        "emoji": "<:twitch:1213233138113708112>",
        "color": 0x9146ff,
        "message": None
    },
    "twitter": {
        "icon_url": "https://img.freepik.com/vecteurs-premium/nouveau-logo-twitter-x-2023-telechargement-vectoriel-du-logo-twitter-x_691560-10796.jpg?w=360",
        "emoji": "<a:Twitter:945123022329741332>",
        "color": 0x05acf0,
        "message": None
    },
    "youtube": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/youtube.png",
        "emoji": "<:youtube:1213233140781551636>",
        "color": 0xfe0000,
        "message": None
    },
    "youtube:tab": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/youtube.png",
        "emoji": "<:youtube:1213233140781551636>",
        "color": 0xfe0000,
        "message": None
    },
    "reddit": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/reddit.png",
        "emoji": "<:reddit:1213231222080413706>",
        "color": 0xff4500,
        "message": None
    },
    "discord": {
        "icon_url": "https://culture-sympathique.fr/discord_imgs/discord.png",
        "emoji": "<:discord:1215742891448733836>",
        "thumbnail": "https://droplr.com/wp-content/uploads/2020/10/Discord-music-e1635364775454.png",
        "color": 0xff4500,
        "message": None
    },
    "générique": {
        "thumbnail": "https://images.frandroid.com/wp-content/uploads/2018/08/guide-apps-video-android.jpg",
        "emoji": "📹",
        "icon_url": "https://cdn0.iconfinder.com/data/icons/basic-uses-symbol-vol-2/100/Help_Need_Suggestion_Question_Unknown-512.png",
        "color": 0xffffff,
        "message": None
    }
}

nsfw_values = { True: ["explicit", "questionable"], False: ["general", "sensitive"] }