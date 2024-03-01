from discord import Embed, Colour, ButtonStyle
import discord.ui as ui
from pybooru import Danbooru

from tools.passwords import danbooru_api
from secrets import token_hex, SystemRandom
from tools.variables import values
from cogs.download import Posts_Button

random = SystemRandom()

def search_on_danbooru(title: str, desc: str, search: str, num_of_query: int, source: str) -> dict:
    if len(search.split()) >= 3:
        return None
    
    dict_of_emb = {}
    errors = 0
    for n in range(num_of_query):
        try:
            search_obj = return_search_object(source).post_list(tags=search, limit=6000)
            img = random.choice(search_obj)
            dict_of_emb[n] = create_embed_and_view(title, desc, img["id"], img["file_url"], source)
        except IndexError:
            return IndexError
        except:
            errors+=1
            continue
        finally:
            dict_of_emb["errors"] = errors
    return dict_of_emb

def create_embed_and_view(title: str, description: str, id: int, img_url: str, source: str) -> list:
    msg = Embed(title=title, description=description, color=Colour.from_str(f"#{token_hex(3)}"))
    msg.set_image(url=img_url)
    msg.set_footer(text=f"Depuis {source} - ID {id}")
    
    view = Posts_Button(timeout=None).add_item(
        ui.Button(label="Lien vers l'image", style=ButtonStyle.link, url=img_url))
    
    return [msg, view]

# Renvoie l'objet pour chercher sur le bon site
def return_search_object(source: str):
    return Danbooru(source, username="Kiri-chan27", api_key=danbooru_api)