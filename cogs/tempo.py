import discord
from discord.ext import commands
from discord import app_commands
from asyncio import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions

maskmania_url = "https://www.paydaythegame.com/payday3/updates/maskmania/"

opts = FirefoxOptions()
opts.add_argument("--headless")

class Temp(commands.GroupCog, name="tempo"):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="maskmania", description="Récupère l'avancée de Mask Mania")
    async def mask(self, react: discord.Interaction):
        await self.bot.wait_until_ready()
        await react.response.defer()
        
        try:
            service = webdriver.FirefoxService(executable_path="/home/tintin/discord_bot/Kiri-chan/exec/geckodriver")
            driver = webdriver.Firefox(service=service, options=opts)
            driver.get(maskmania_url)
        except Exception as e:
            print(e)

        try:
            element1 = driver.find_elements(By.CSS_SELECTOR, 'div.lastmaskconceptprogress[data-mask="GearheadGrudge"]')
            element2 = driver.find_elements(By.CSS_SELECTOR, 'div.lastmaskconceptprogress[data-mask="ShakedownShark"]')
            element3 = driver.find_elements(By.CSS_SELECTOR, 'div.lastmaskconceptprogress[data-mask="CutIce"]')
            element4 = driver.find_elements(By.CSS_SELECTOR, 'div.lastmaskconceptprogress[data-mask="DiscoMolly"]')
            
            await react.followup.send(f"Avancée de l'Event:\n<:gearheadgrudge:1262939375906324511> GEARHEAD GRUDGE: {element1[0].get_attribute('data-label')}\n<:cutice:1262939270360862740> CUT ICE: {element3[0].get_attribute('data-label')}\n<:shakedownshark:1262939272034385920> SHAKEDOWN SHARK: {element2[0].get_attribute('data-label')}\n<:discomolly:1262939401084866620> DISCO MOLLY: {element4[0].get_attribute('data-label')}")

        except Exception as e:
            await react.followup.send("Erreur de récup.")

        finally:
            driver.quit()
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Temp(bot))