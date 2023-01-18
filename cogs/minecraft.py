import discord
from discord.ext import commands

class Minecraft(commands.Cog, name="Minecraft module"):
    def __init__(self, bot):
        self.bot = bot
        
    # Commands for Minecraft Server
    @commands.command(name="getRole", aliases=['getrole', 'gr'])
    async def getRole(self, ctx, role_name):
        await ctx.message.delete()
        list_of_non_roles = ["Modoux", "Kirlia-chan", "Bots"]

        guild = ctx.guild
        member = ctx.message.author
        if guild.id != 682267012709613580:
            await member.send("Cette commande n'est pas disponible pour ce serveur.")
            return
        elif role_name.capitalize() in list_of_non_roles:
            await member.send("Tu ne peux pas obtenir ce rôle.")
            return
    
        role = discord.utils.get(guild.roles, name = role_name.capitalize())
        await member.add_roles(role)

    # Command to remove a role from a user
    @commands.command(name="removeRole", aliases=['removerole', 'rr', 'rmrole'])
    async def removeRole(self, ctx, role_name):
        await ctx.message.delete()
        guild = ctx.guild
        member = ctx.message.author
        if guild.id != 682267012709613580:
            await member.send("Cette commande n'est pas disponible pour ce serveur.")
            return
    
        roles = discord.utils.find(lambda r: r.name == 'Member', ctx.message.guild.roles)
        if roles not in member.roles:
            await member.send(f"Tu ne possède pas le rôle {role_name.capitalize()}.")
            return
        role_get = discord.utils.get(guild.roles, name = role_name.capitalize())
        await member.remove_roles(role_get)
        
async def setup(bot):
    await bot.add_cog(Minecraft(bot))