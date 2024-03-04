import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands, ButtonStyle, SelectOption
from discord.ui import button, Button, View, Select

from os import listdir, remove, path, mkdir
import random
import urllib.request
from zipfile import ZipFile, ZIP_DEFLATED
from tools.paths import nekodata_path, web_path
from shutil import rmtree
import re

class Image_Viewer():
    
    def __init__(self, user: discord.User, link_list: list) -> None:
        self.embed = None
        self.view = None
        self.user = user
        self.curlink = ""
        self.pagecur = 0
        self.page_max = 0
        self.current_in_selectoption = 0
        self.curall = 0
        self.max = 0
        self.link_list = link_list
        self.page_dict = None
        self.select_list = None
    
    def _get_message(self, creation:bool=True) -> list:
        if creation:
            self.page_dict = self._create_dict()
            self.max = len(self.link_list)
        self.current_list = self.page_dict[self.pagecur]
        self.curlink = self.link_list[self.curall]
        self.embed = self._create_embed()
        self.view = self._create_view()
        return [self.embed, self.view]
    
    def _create_dict(self) -> dict:
        page_dict = {}
        page_limit = 20
        self.page_max = int(len(self.link_list)/page_limit)
        
        for num in range(self.page_max+1):
            page_dict[num] = self._create_select_list(self.link_list[num*page_limit:(num+1)*page_limit], num*page_limit)
        return page_dict
        
    def _create_select_list(self, link_list: list, start_num: int) -> dict:
        select_list = []
        for num, link in enumerate(link_list):
            if num == self.current_in_selectoption:
                is_default = True
            else:
                is_default = False
            select_list.append(discord.SelectOption(label=f"Élément {start_num+num+1}", description=link, emoji="🖼️", default=is_default))
        if self.pagecur > 0:
            select_list.append(discord.SelectOption(label=f"Page précédente", emoji="⬅️"))
        if self.pagecur < self.page_max:
            select_list.append(discord.SelectOption(label=f"Page suivante", emoji="➡️"))
        return select_list
        
    def _create_embed(self):
        return Embed(title=f"📋 [{self.curall+1}/{self.max}] - Liste de {self.user.display_name}",description=None,color=self.user.color).set_image(url=self.curlink).set_footer(text="Depuis la liste du NekoBot")
    
    def _create_view(self) -> View:
        view = View(timeout=None)
        
        select_menu = Select(
            placeholder="Choisis une image",
            max_values=1,
            min_values=1,
            options=self.current_list)
        delete_button = Button(label="Supprimer", style=ButtonStyle.danger, emoji="🗑️")
        web_button = Button(label="Lien vers l'image", style=ButtonStyle.link, url=self.curlink)
        quit_button = Button(label="Fermer", style=ButtonStyle.danger, emoji="<:disconnect_icon:1148310144703279134>")
                
        async def menu_callback(react: discord.Interaction) -> None:
            await react.response.defer(thinking=False)
            
            if select_menu.values[0] == "Page précédente":
                self.pagecur-=1
                self.current_in_selectoption = -1
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
            elif select_menu.values[0] == "Page suivante":
                self.pagecur+=1
                self.current_in_selectoption = -1
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
            else:
                self.current_in_selectoption = int((re.search(r'\d+$', select_menu.values[0]).group()) if re.search(r'\d+$', select_menu.values[0]) else None) - (self.pagecur*20) -1
                self.curall = int((re.search(r'\d+$', select_menu.values[0]).group()) if re.search(r'\d+$', select_menu.values[0]) else None) -1
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
           
        async def delete_callback(react: discord.Interaction):
            link = react.message.embeds[0].image.url
            result = delete_link(f"{nekodata_path}{react.user.id}/list.txt", link)
            if result:
                await react.response.send_message("✅ Image supprimée !", ephemeral=True)
            else:
                await react.response.send_message("❌ Impossible de supprimer cette image...", ephemeral=True)
                
            if self.max <= 1:
                # Cas où il n'y a plus de liens dans la liste
                await react.message.delete()
                await react.followup.send("Il n'y a plus d'images dans ta liste, le lecteur d'image s'est fermé.", ephemeral=True)
            else:
                self.link_list = load_file(f"{nekodata_path}{react.user.id}/list.txt")
                self.curall-=1
                self.current_in_selectoption-=1
                msg = self._get_message(creation=True)
                await react.message.edit(embed=msg[0], view=msg[1])
        
        async def quit_callback(react: discord.Interaction):
            return await react.message.delete()
        
        select_menu.callback = menu_callback
        delete_button.callback = delete_callback
        quit_button.callback = quit_callback
        view.add_item(select_menu).add_item(web_button).add_item(delete_button).add_item(quit_button)
    
        return view
     

class Posts_Button(View):
    
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        
    @button(label="Ajouter à ta liste", style=ButtonStyle.success, emoji="📝")
    async def add_to_list(self, react: discord.Interaction, button: Button):
        id = react.user.id
        link = react.message.embeds[0].image.url
        
        try:
            if not path.exists(f"{nekodata_path}{id}"):
                mkdir(f"{nekodata_path}{id}")
            with open(f"{nekodata_path}{id}/list.txt", "a") as file:
                file.write(f"{link}\n")
            return await react.response.send_message("✅ Ajouté à ta liste !", delete_after=15, ephemeral=True)
        except:
            return await react.response.send_message("❌ Impossible de l'ajouter à la liste...", delete_after=15, ephemeral=True)

class Download(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="download", description="Télécharge les images de ta liste dans un fichier zip.")
    async def dl_func(self, react: discord.Interaction) -> None:
        
        # Vérifie si la dossier de l'utilisateur existe
        if not path.exists(f"{nekodata_path}{react.user.id}/list.txt"):
            return await react.response.send_message("Erreur: Ta liste ne contient aucune image.", ephemeral=True)

        await react.response.defer(ephemeral=True)
        user_folder = f"{nekodata_path}{react.user.id}"
        
        download_list = []
        with open(f"{user_folder}/list.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                download_list.append(line)
        
        error_num = 0
        for current_img, link in enumerate(download_list):
            try:
                urllib.request.urlretrieve(link, f"{user_folder}/image_{current_img}.png")
            except:
                error_num += 1
        
        if error_num == len(download_list):
            return await react.followup.send("Impossible de télécharger les images.")
        
        # Génère un nombre aléatoire pour ce fichier zip
        zip_name = random.SystemRandom().randint(100, 99999999)
        
        if path.exists(f"{web_path}{zip_name}.zip"):
            remove(f"{web_path}{zip_name}.zip")
        
        with ZipFile(f"{web_path}{zip_name}.zip", "w", ZIP_DEFLATED) as zobj:
            for img in listdir(f"{user_folder}"):
                if img == "list.txt":
                    continue
                zobj.write(f"{user_folder}/{img}", img, ZIP_DEFLATED)
        
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="Lien vers l'archive", style=discord.ButtonStyle.link, url=f"http://www.culture-sympathique.fr/images/{zip_name}.zip"))
        
        await react.followup.send(content="Consulte tes DM pour obtenir le lien.", ephemeral=True)
        await react.user.send(content=f"✅ Téléchargement terminé ! Nombre d'erreur(s): {error_num}. (Archive **{zip_name}**)", view=view)
        
        # Suppresion des fichiers
        rmtree(user_folder)
        
    @app_commands.command(name="list", description="Affiche la liste de tes images.")
    async def list(self, react: discord.Interaction):
        if not path.exists(f"{nekodata_path}{react.user.id}/list.txt") or path.getsize(f"{nekodata_path}{react.user.id}/list.txt") == 0:
            return await react.response.send_message("Ta liste ne contient aucune image.", ephemeral=True)
        
        img_list = load_file(f"{nekodata_path}{react.user.id}/list.txt")
        
        viewer = Image_Viewer(react.user, img_list)
        message = viewer._get_message()
        
        await react.response.send_message(embed=message[0], view=message[1])
    
def delete_link(file_path, link_to_delete) -> bool:
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        # Supprimer le lien spécifié s'il existe dans la liste
        lines.pop(lines.index(link_to_delete + '\n'))

        with open(file_path, 'w') as f:
            f.writelines(''.join(lines))
        return True
    except:
        return False

# Lis ligne par ligne le contenu d'un fichier
def load_file(file_path) -> list:
    file_list = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            file_list.append(line)
    return file_list
        
async def setup(bot):
    await bot.add_cog(Download(bot))