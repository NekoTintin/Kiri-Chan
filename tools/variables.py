from typing import Literal

# Dictionnaire qui stocke les cogs chargés
loaded_ext = list()

online_message = "Salut mon pote !"
ver_num = "2.1.3"

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

sites_dict = {
    "dailymotion.com": {
        "thumbnail_url": "https://www.dailymotion.com/thumbnail/video/vid_id",
        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/2/27/Logo_dailymotion.png",
        "color": 0x00bff9
    },
    "deezer.com": {
        "thumbnail_url": "",
        "icon_url": "http://store-images.s-microsoft.com/image/apps.10845.13510798886741797.23acf55e-f23e-46de-a8cf-654b578e5620.e6cbedec-19c0-4caa-be7d-5e54baa2ec71",
        "color": 0xffffff
    },
    "soundcloud.com": {
        "thumbnail_url": "https://dreamityourselfmusician.com/wp-content/uploads/2022/01/soundcloud.png",
        "icon_url": "https://play-lh.googleusercontent.com/lvYCdrPNFU0Ar_lXln3JShoE-NaYF_V-DNlp4eLRZhUVkj00wAseSIm-60OoCKznpw=w240-h480",
        "color": 0xff6800
    },
    "tiktok.com": {
        "thumbnail_url": "https://c0.lestechnophiles.com/www.numerama.com/wp-content/uploads/2018/11/tik-tok-680x383.jpg?resize=500,281&key=86eeaf48",
        "icon_url": "https://cdn.pixabay.com/photo/2021/06/15/12/28/tiktok-6338432_960_720.png",
        "color": 0xee1d52
    },
    "twitch.com": {
        "thumbnail_url": "https://static.latribune.fr/1780917/twitch.jpg",
        "icon_url": "https://pbs.twimg.com/profile_images/1290231731056971776/67hU0Sgv_400x400.png",
        "color": 0x9146ff
    },
    "twitter.com": {
        "thumbnail_url": "https://pic.clubic.com/v1/images/1941993/raw",
        "icon_url": "https://e7.pngegg.com/pngimages/804/985/png-clipart-social-media-logo-computer-icons-information-twitter-logo-media.png",
        "color": 0x05acf0
    },
    "youtube.com": {
        "thumbnail_url": "https://i3.ytimg.com/vi/vid_id/maxresdefault.jpg",
        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Youtube-logo-red.png",
        "color": 0xfe0000
    }
}