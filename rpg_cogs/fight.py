import discord
from discord.ext import commands
from discord import app_commands
from discord.embeds import Embed
from discord.ui import Button, View

from typing import Literal
from asyncio import sleep

path = "/home/Tintin/discord_bot/Kiri-chan/rpg_cogs/"
ffmpeg_opts = {'options': '-vn'}

class Fight(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice = None
        super().__init__()
        
    """
    @app_commands.command(name="fight", description="C'est l'heure de la bagarre !")
    async def fight(self, interaction: discord.Interaction, adversaire: discord.User, lieu: Literal["Arene", "Ring de Boxe", "Orphelinat"], armes: Literal["Couteau", "Gun", "La prothèse de Kor1, votre cher dictateur qui a acheté une prothèse alors qui a tous ses bras ce..."], secondaire: Literal["Soins Médicaux", "Des explosifs de Jimmy", "Le Damien Juice(TM)"], soutien_psy: Literal["Ben Laden", "Le vieux SDF au coin de la rue", "Philipe Etjtebeze"], background: Literal["Général", "Techno", "Pro"], super_héro_préféré: Literal["Epileptique-Man", "Nicolas Sarkozy", "Gégé du PMU"], religion: Literal["Prie Kaname Madoka", "Prie Black Jesus, the mother fucking christ", "La Sainte Barbe"], bord_politique: Literal["Droite", "Droite !", "Droite ?"], animal: Literal["Chien", "Chat", "Joshua Navarre"]) -> None:
        await interaction.response.defer()
        
        await sleep(10)
        
        await interaction.followup.send("SEXSEAL a perdu parce qu'il est inintéressant.")
    """
    
    @app_commands.guild_only()
    @app_commands.guilds(759147102093049876)
    @app_commands.command(name="fight", description="C'est l'heure de la bagarre !")
    async def fight(self, interaction: discord.Interaction, adversaire: discord.User):
        await interaction.response.defer()
        
        if adversaire.id == 592750256899489825:
            msg = Embed(title="C'est l'heure du du-du-du-du-Duel !", description="KOR1, THE SYMPATHIQUE DICTATOR !!!! et une barre de vie apparaissent !", color=0xff00ff)
            msg.set_footer(text="Kiri-chan: The Promised Neverlands of Jojo !", icon_url="https://images-ext-1.discordapp.net/external/7Yhla3kMaxtVKEFZIv9vOuDWsLeA8-pSvB2AFyYeNr4/%3Fsize%3D4096%26ignore%3Dtrue/https/cdn.discordapp.com/avatars/789984188224110632/b06507f8de4e4883b8fac4b2330cbb5b.png?width=634&height=634")
            file = discord.File(f"{path}images/dictator/dictateurBoss.png", filename="image.png")
            msg.set_image(url="attachment://image.png")
            msg.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1732/1732476.png")
            
            guild = interaction.guild
            try:
                channel = interaction.user.voice.channel
                
                if self.voice == None:
                    await channel.connect()
                    self.voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        
                if self.voice.is_playing():
                    self.voice.stop()
            
                self.voice.play(discord.FFmpegOpusAudio(f"{path}musics/dictator_theme.mp3"))
            except:
                pass
            
            
            view = View(timeout=None)
            attack_button = Button(label="Attaque !", style=discord.ButtonStyle.green, emoji="⚔️")
            defense_button = Button(label="Se défendre", style=discord.ButtonStyle.green, emoji="🛡️")
            magie_button = Button(label="Magie", style=discord.ButtonStyle.danger, emoji="🪄")
            
            view.add_item(attack_button).add_item(defense_button).add_item(magie_button)
            
            
            await interaction.followup.send(embed=msg, file=file, view=view)
            
        
async def setup(bot):
    await bot.add_cog(Fight(bot))
    
