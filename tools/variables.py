from typing import Literal
from secrets import token_hex
from discord import Color

# Dictionnaire qui stocke les cogs chargés
loaded_ext = list()

online_message = "toujours plus de vidéos sur Youtube"
ver_num = "3.2.0"

# Fonction pour obtenir les modules chargés
def get_modules() -> list():
    l = list()
    for filename in loaded_ext:
        l.append(filename)
    return l

def add_module(name):
    loaded_ext.append(name)
    
def remove_module(name):
    loaded_ext.remove(name)

# Liste des valeurs pour les commandes
values = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]

# Sites bannis
ban_domain = ["spotify", "deezer", "PornHub", "youporn"]

sites_dict = {
    "dailymotion": {
        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/2/27/Logo_dailymotion.png",
        "color": 0x00bff9,
        "message": None
    },
    "soundcloud": {
        "icon_url": "https://play-lh.googleusercontent.com/lvYCdrPNFU0Ar_lXln3JShoE-NaYF_V-DNlp4eLRZhUVkj00wAseSIm-60OoCKznpw=w240-h480",
        "color": 0xff6800,
        "message": None
    },
    "tiktok": {
        "icon_url": "https://cdn.pixabay.com/photo/2021/06/15/12/28/tiktok-6338432_960_720.png",
        "color": 0xee1d52,
        "message": None
    },
    "twitch": {
        "icon_url": "https://pbs.twimg.com/profile_images/1290231731056971776/67hU0Sgv_400x400.png",
        "color": 0x9146ff,
        "message": None
    },
    "twitter": {
        "icon_url": "https://e7.pngegg.com/pngimages/804/985/png-clipart-social-media-logo-computer-icons-information-twitter-logo-media.png",
        "color": 0x05acf0,
        "message": None
    },
    "youtube": {
        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Youtube-logo-red.png",
        "color": 0xfe0000,
        "message": None
    },
    "générique": {
        "thumbnail": "https://images.frandroid.com/wp-content/uploads/2018/08/guide-apps-video-android.jpg",
        "icon_url": "https://cdn0.iconfinder.com/data/icons/basic-uses-symbol-vol-2/100/Help_Need_Suggestion_Question_Unknown-512.png",
        "color": Color.from_str(f"#{token_hex(3)}"),
        "message": None
    }
}

keywords = ["général", "meme", "accueil", "seal-zone", "bienvenue"]