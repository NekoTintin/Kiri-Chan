# -- coding: utf-8 --

# Biblio de Discord
import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import app_commands

# Autres
import subprocess

# Module du bot
import tools.variables as var

from typing import Literal

mods_list = Literal["AdReplacer", "ArtGallery", "Crypto-Fanta", "PeppaPig3"]

class Tools(commands.GroupCog, name="tools"):
    
    # Méthode d'initialisation de la classe (avec bot an argument).
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
    # Commandes Outils/Tools
    # Retourne la latence
    @app_commands.command(name="ping", description="Affiche la latence.")
    async def ping(self, react: discord.Interaction):
        await react.response.send_message(f"Pong ! - La latence est de: **{self.bot.latency * 1000}** millisecondes.", ephemeral=True)
    
    # Retourne la version
    @app_commands.command(name="version", description="Obtiens le numéro de version")
    async def version(self, react: discord.Interaction) -> None:
        await react.response.send_message(f"Je suis en version: **{var.ver_num}** !", ephemeral=True)
    
    # Renvoie un lien vers le repo GitHub
    @app_commands.command(name="github", description="Lien vers le repo sur GitHub.")
    async def git(self, react: discord.Interaction):
        message = Embed(title="Lien du GitHub:", color=0xfbfcfc).add_field(name="Repo de Kiri-Chan:", value="https://github.com/Tintin361/Kiri-chan")\
        .add_field(name="Repo de Little Kyubey", value="https://github.com/Tintin361/Lil_Kyubey")\
        .add_field(name="Repo de NekoBot", value="https://github.com/Tintin361/NekoBot")\
        .add_field(name="Repo de VeemoBot", value="https://github.com/Tintin361/VeemoBot")
        await react.response.send_message(embed=message, ephemeral=True)
        
    # Envoie des commandes en Bash
    @app_commands.command(name="syscom", description="Envoie un commande vers l'OS")
    async def syscom(self, react: discord.Interaction, command: str):
        await self.bot.wait_until_ready()
        
        if react.user.id != 443113150599004161:
            return
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            output = result.stdout.strip() if result.stdout else "Pas de résultat"
            await react.response.send_message(f"Sortie:\n{output[:1950]}")
        except subprocess.CalledProcessError:
            await react.response.send_message(f"Erreur lors de l'exécution de la commande `{command}`")
            
    @app_commands.command(name="selfnick", description="Pas touche à ça !")
    async def selfnick(self, react: discord.Interaction, nick: str):
        if react.user.id == var.nekotintin_id:
            await react.guild.get_member(self.bot.user.id).edit(nick=nick)
            return await react.response.send_message("C'est fait !", ephemeral=True)
        await react.response.send_message("Pas touche à ça !", ephemeral=True)
        
    @app_commands.command(name="envoyer", description="Envoie un message pour informer d'une MàJ de mod.")
    async def _send_update(self, react: discord.Interaction, mod: mods_list, version: float, url: str, contenu: str) -> None:
        await self.bot.wait_until_ready()
        
        if react.user.id != 443113150599004161:
            return await react.response.send_message("Tu ne peux pas utiliser cette commande.", ephemeral=True)
        
        msg = Embed(title=f"Mise à jour du **{mod}**",
                    description=f"La version *{version}* est disponible à cette URL: {url}",
                    color=0x0d7ecd, url=url)
        msg.add_field(name="Contenu de la MàJ", value=contenu, inline=False)
        msg.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar)
        
        await react.response.send_message(embed=msg)

# Fonction pour ajouter le cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tools(bot))