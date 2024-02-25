from typing import Literal

ver_num = "3.4.0"
online_message = "Sploon 3"

mods = {}

def enable_module(mod):
    mods[mod] = "✅"
    
def disable_module(mod):
    mods[mod] = "❌"
    
def get_modules():
    return mods
    
ban_domain = ["twitter", "deezer", "spotify"]

values = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]
    
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
        "icon_url": "https://static-00.iconduck.com/assets.00/twitch-icon-2048x2048-tipdihgh.png",
        "color": 0x9146ff,
        "message": None
    },
    "twitter": {
        "icon_url": "https://e7.pngegg.com/pngimages/804/985/png-clipart-social-media-logo-computer-icons-information-twitter-logo-media.png",
        "color": 0x05acf0,
        "message": None
    },
    "youtube": {
        "icon_url": "https://cdn.icon-icons.com/icons2/1099/PNG/512/1485482355-youtube_78661.png",
        "color": 0xfe0000,
        "message": None
    },
    "reddit": {
        "icon_url": "https://freelogopng.com/images/all_img/1658834272reddit-logo-transparent.png",
        "color": 0xff4500,
        "message": None
    },
    "générique": {
        "thumbnail": "https://images.frandroid.com/wp-content/uploads/2018/08/guide-apps-video-android.jpg",
        "icon_url": "https://cdn0.iconfinder.com/data/icons/basic-uses-symbol-vol-2/100/Help_Need_Suggestion_Question_Unknown-512.png",
        "color": 0xffffff,
        "message": None
    }
}