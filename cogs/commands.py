import discord
from discord.exe import commands
import platform

import cogs._json

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Les Rouages sont Lancées")

    
    @commands.command()
    @commands.is_owner()
    async def openjson(ctx, jsonfile):
        data = read_json(f"{jsonfile}")
        #data.replace("\'",'\"')
        await ctx.send(f" ```json\n{data}``` ")
    
    @commands.command()
    @commands.is_owner()
    async def blacklist(ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send('Tu ne peux pas te blacklist toi meme')
            return
        if bot.user.id == user.id:
            await ctx.send('Tu ne peux pas me blacklist ')
            return
        bot.blacklisted_users.append(user.id)
        data = read_json("blacklist")
        data["user"].append(user.id)
    
        write_json(data, "blacklist")
    
        await ctx.send(f"Je viens de Blacklist ``{user.name}`` de mon service.")
    
    @commands.command()
    @commands.is_owner()
    async def unblacklist(ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send('Tu ne peux pas te retiré de la Blacklist toi meme')
            return
        bot.blacklisted_users.remove(user.id)
        data = read_json("blacklist")
        data["user"].remove(user.id)
        write_json(data, "blacklist")
    
        await ctx.send(f"Je viens de retiré de la Blacklist ``{user.name}`` de mon service.")
    
    @commands.command(name='botinfo', aliases=['bi'])
    async def stats(ctx):
        """
        Afficher les Stats du bot
        """
        data = read_json("info")
        fichierInfo = data
        fichierInfo['pythonVersion'] = platform.python_version()
        fichierInfo['dPyVersion'] = discord.__version__
        fichierInfo['serverCount'] = len(bot.guilds)
        fichierInfo['memberCount'] = len(set(bot.get_all_members()))
    
        statEmbed = discord.Embed(tiltle = f'{bot.user.name} Stats', description = '\uFEFF', colour = ctx.author.colour, timestamp = ctx.message.created_at)
    
        statEmbed.add_field(name='Bot Version', value=fichierInfo['BotVersion'])
        statEmbed.add_field(name='Python Version', value=fichierInfo['pythonVersion'])
        statEmbed.add_field(name='Discord Python Version', value=fichierInfo['dPyVersion'])
        statEmbed.add_field(name='Nombre Serveur', value=fichierInfo['serverCount'])
        statEmbed.add_field(name='Nombre Membre', value=fichierInfo['memberCount'])
        statEmbed.add_field(name='Developper', value=f"<@{fichierConfig['owner']['ID']}> alias {fichierConfig['owner']['name']}")
    
        statEmbed.set_footer(text=f'{bot.user.name}')
        statEmbed.set_author(name=f'Stats', icon_url=ctx.author.avatar_url)
    
        await ctx.send(embed=statEmbed)
        
    @commands.command(aliases=['disconnect', 'stopBot'])
    @commands.is_owner()
    async def logout(ctx):
        """
        Stopper le Bot
        """
        await ctx.send(f"Déconnection en Cours")
        await bot.logout()
    
    @logout.error
    async def logout_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Tu n'as pas les Permission pour stopper ce bot")