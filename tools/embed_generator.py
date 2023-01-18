from discord.embeds import Embed
from discord import File

# Transforme un dictonnaire en message Embed Discord
def gen_embed(params: dict) -> Embed and File or Embed and None:
    message = Embed(title=params["title"], description=params["description"], color=params["color"])
    
    if len(params) >= 7:
        for item in range(6, len(params)):
            message.add_field(name=params[item].keys(), value=params[item]["content"], inline=params[item]["inline"])
        
    # Vérifie si le message doit contenir une image
    if params["image"] == True:
        message.set_image(url="attachment://" + params["image"]["name"])
        file = File(params["image"]["path"] + params["image"]["name"])
        
        return message, file
    
    return message, None


def gen_embed_yt(params: dict) -> Embed and File:
    message = Embed(title=params["title"], description=params["description"], color=params["color"])
        
    message.set_image(url="attachment://" + params["image"]["name"])
    file = File(params["image"]["path"] + params["image"]["name"])
        
    return message, file