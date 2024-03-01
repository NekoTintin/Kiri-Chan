import discord
from discord import Embed, ButtonStyle
from discord.ui import Button, View, Select
import re
import requests

from secrets import token_hex, SystemRandom
from cogs.download import Posts_Button

rating_dict = { "g": "General", "s": "Sensitive", "q": "Questionable", "e": "Explicit" }

random = SystemRandom()

def _create_request(tags: str) -> dict:
    headers = { "Accept": "application/json" }
    resp = requests.get("https://danbooru.donmai.us/posts/random", params=tags, headers=headers)
    
    if resp.status_code == 200:
        return resp.json()
    else:
        return None


class Image_Viewer():
    
    def __init__(self, img_list: dict, title: str, desc: str, search: str, rating: list) -> None:
        self.embed = None
        self.view = None
        self.curlink = ""
        self.pagecur = 0
        self.page_max = 0
        self.current_in_selectoption = 0
        self.curall = 0
        self.max = 0
        self.img_list = img_list
        self.page_dict = None
        self.select_list = None
        self.title = title
        self.desc = desc
        self.search = search
        self.rating = rating
    
    def _get_message(self, creation:bool=True) -> list:
        if creation:
            self.page_dict = self._create_dict()
            self.max = len(self.img_list)
        self.current_list = self.page_dict[self.pagecur]
        self.curlink = self.page_dict[self.pagecur][self.current_in_selectoption].description
        self.embed = self._create_embed()
        self.view = self._create_view()
        return [self.embed, self.view]
    
    def _create_dict(self) -> dict:
        page_dict = {}
        page_limit = 20
        self.page_max = int(len(self.img_list)/page_limit)
        
        for num in range(self.page_max+1):
            page_dict[num] = self._create_select_list(self.img_list[num*page_limit:(num+1)*page_limit], num*page_limit)
        return page_dict
        
    def _create_select_list(self, img_list: list, start_num: int) -> dict:
        select_list = []
        for num, link in enumerate(img_list):
            if link == 0:
                continue
            select_list.append(discord.SelectOption(label=f"Image {start_num+num+1}", description=link["file_url"][:100], emoji="🖼️"))
        if self.pagecur > 0:
            select_list.append(discord.SelectOption(label=f"Page précédente", emoji="⬅️"))
        if self.pagecur < self.page_max:
            select_list.append(discord.SelectOption(label=f"Page suivante", emoji="➡️"))
        return select_list
        
    def _create_embed(self):
        emb = Embed(title=f"📋 [{self.curall+1}/{self.max-1}]", description=f"{self.desc}", color=0xFF5700)
        emb.set_image(url=self.curlink)
        emb.set_footer(text=f"ID {self.img_list[self.curall]['id']} - Rating {'/'.join(self.rating)}")
        
        return emb
    
    def _create_view(self) -> View:
        view = Posts_Button(timeout=None)
        
        select_menu = Select(placeholder="Choisis une image", max_values=1, min_values=1, options=self.current_list)
        web_button = Button(label="Lien vers l'image", style=ButtonStyle.link, url=self.curlink)
        quit_button = Button(label="Fermer", style=ButtonStyle.danger, emoji="<:disconnect_icon:1148310144703279134>")
                
        async def menu_callback(react: discord.Interaction) -> None:
            await react.response.defer(thinking=False)
            
            if select_menu.values[0] == "Page précédente":
                self.pagecur-=1
                self.current_in_selectoption = 0
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
            elif select_menu.values[0] == "Page suivante":
                self.pagecur+=1
                self.current_in_selectoption = 0
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
            else:
                self.current_in_selectoption = int((re.search(r'\d+$', select_menu.values[0]).group()) if re.search(r'\d+$', select_menu.values[0]) else None) - (self.pagecur*20) -1
                self.curall = int((re.search(r'\d+$', select_menu.values[0]).group()) if re.search(r'\d+$', select_menu.values[0]) else None) -1
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
        
        async def quit_callback(react: discord.Interaction):
            return await react.message.delete()
        
        select_menu.callback = menu_callback
        quit_button.callback = quit_callback
        view.add_item(select_menu).add_item(web_button).add_item(quit_button)
    
        return view
    

def search_on_danbooru(title: str, desc: str, search: str, num_of_query: int, rating_list: list) -> list:
    if len(search.split()) >= 3:
        return None
    
    list_of_img = []
    errors = 0
    for _ in range(num_of_query):
        try:
            img = _create_request({"tags": f"{search} rating:{','.join(rating_list)}"})
            if img == []:
                errors+=1
                continue
            list_of_img.append(img)
        except:
            errors+=1
            continue
    list_of_img.append(errors)
    
    viewer = Image_Viewer(list_of_img, title, desc, search, rating_list)
    return viewer._get_message()