# Libs
#pip install [discord]
import discord
from discord.ext import commands
import logging
from pathlib import Path
import platform
import json
import os

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Defining a few things
fichierSecret = json.load(open(cwd+'/Config/secrets.json'))
fichierConfig = json.load(open(cwd+'/Config/config.json'))
fichierInfo = json.load(open(cwd+'/Config/info.json'))
bot = commands.Bot(command_prefix=fichierConfig['prefix'], case_insensitive=True, owner_id=int(fichierConfig['owner']['ID']))
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []

@bot.event
async def on_ready():
    # Another way to use variables in strings
    print("\n\nBot:\n\tNom:\t{}\n\tID:\t{}\n\tPrefix:\t{}".format(bot.user.name, bot.user.id, fichierConfig['prefix']))
    print("\nOwner :\n\tNom:\t{}\n\tID:\t{}".format(fichierConfig['owner']['name'], fichierConfig['owner']['ID']))
    await bot.change_presence(activity=discord.Game(name=f"-help")) # This changes the bots 'activity'

#    data = read_json("blacklist")
#    bot.blacklisted_users = data["user"]

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if message.author.id in bot.blacklisted_users:
        return
    await bot.process_commands(message)

if __name__ == '__main__':
    if not os.path.exists('cogs'):
        os.makedirs('cogs')
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

#@bot.event
#async def on_command_completion(ctx):
#    data = read_json("info")
#    data['pythonVersion'] = platform.python_version()
#    data['dPyVersion'] = discord.__version__
#    data['serverCount'] = len(bot.guilds)
#    data['memberCount'] = len(set(bot.get_all_members()))
#    data["nbCommandeUtilise"] = data["nbCommandeUtilise"]+1
#    write_json(fichierInfo, "info")
#    print(f'OUI {ctx.message}\n{fichierInfo}')
#
#@bot.event
#async def on_command_error(ctx, error):
#    ignorer = (commands.CommandNotFound, commands.UserInputError)
#    if isinstance(error, ignorer):
#        return
#    if isinstance(error, commands.CommandOnCooldown):
#        m, s = divmod(error.retry_after, 60)
#        h, m = divmod(m, 60)
#        if int(h) is 0 and int(m) is 0:
#            await ctx.send(f'tu devrais attendre {int(s)}s avant de réutiliser cette commande !')
#        elif int(h) is 0 and int(m) is not 0:
#            await ctx.send(f'tu devrais attendre {int(m)}m {int(s)}s avant de réutiliser cette commande !')
#        else:
#            await ctx.send(f'tu devrais attendre {int(h)}h {int(m)}m {int(s)}s avant de réutiliser cette commande !')
#    elif isinstance(error, commands.CheckFailure):
#        await ctx.send("Tu n'as pas les Permission pour utiliser cette commands.")
#    raise error
#
#@bot.event
#async def on_message(message):
#    if message.author.id == bot.user.id:
#        return
#    if message.author.id in bot.blacklisted_users:
#        return
#    await bot.process_commands(message)
#
#@bot.command()
#@commands.is_owner()
#async def openjson(ctx, jsonfile):
#    data = read_json(f"{jsonfile}")
#    #data.replace("\'",'\"')
#    await ctx.send(f" ```json\n{data}``` ")
#
#@bot.command()
#@commands.is_owner()
#async def blacklist(ctx, user: discord.Member):
#    if ctx.message.author.id == user.id:
#        await ctx.send('Tu ne peux pas te blacklist toi meme')
#        return
#    if bot.user.id == user.id:
#        await ctx.send('Tu ne peux pas me blacklist ')
#        return
#    bot.blacklisted_users.append(user.id)
#    data = read_json("blacklist")
#    data["user"].append(user.id)
#
#    write_json(data, "blacklist")
#
#    await ctx.send(f"Je viens de Blacklist ``{user.name}`` de mon service.")
#
#@bot.command()
#@commands.is_owner()
#async def unblacklist(ctx, user: discord.Member):
#    if ctx.message.author.id == user.id:
#        await ctx.send('Tu ne peux pas te retiré de la Blacklist toi meme')
#        return
#    bot.blacklisted_users.remove(user.id)
#    data = read_json("blacklist")
#    data["user"].remove(user.id)
#    write_json(data, "blacklist")
#
#    await ctx.send(f"Je viens de retiré de la Blacklist ``{user.name}`` de mon service.")
#
#@bot.command(name='botinfo', aliases=['bi'])
#async def stats(ctx):
#    """
#    Afficher les Stats du bot
#    """
#    data = read_json("info")
#    fichierInfo = data
#    fichierInfo['pythonVersion'] = platform.python_version()
#    fichierInfo['dPyVersion'] = discord.__version__
#    fichierInfo['serverCount'] = len(bot.guilds)
#    fichierInfo['memberCount'] = len(set(bot.get_all_members()))
#
#    statEmbed = discord.Embed(tiltle = f'{bot.user.name} Stats', description = '\uFEFF', colour = ctx.author.colour, timestamp = ctx.message.created_at)
#
#    statEmbed.add_field(name='Bot Version', value=fichierInfo['BotVersion'])
#    statEmbed.add_field(name='Python Version', value=fichierInfo['pythonVersion'])
#    statEmbed.add_field(name='Discord Python Version', value=fichierInfo['dPyVersion'])
#    statEmbed.add_field(name='Nombre Serveur', value=fichierInfo['serverCount'])
#    statEmbed.add_field(name='Nombre Membre', value=fichierInfo['memberCount'])
#    statEmbed.add_field(name='Developper', value=f"<@{fichierConfig['owner']['ID']}> alias {fichierConfig['owner']['name']}")
#
#    statEmbed.set_footer(text=f'{bot.user.name}')
#    statEmbed.set_author(name=f'Stats', icon_url=ctx.author.avatar_url)
#
#    await ctx.send(embed=statEmbed)
#    
#@bot.command(aliases=['disconnect', 'stopBot'])
#@commands.is_owner()
#async def logout(ctx):
#    """
#    Stopper le Bot
#    """
#    await ctx.send(f"Déconnection en Cours")
#    await bot.logout()
#
#@logout.error
#async def logout_error(ctx, error):
#    if isinstance(error, commands.CheckFailure):
#        await ctx.send("Tu n'as pas les Permission pour stopper ce bot")
#
#@bot.command()
#async def echo(ctx, *, message=None):
#    """
#    A simple command that repeats the users input back to them.
#    """
#    message = message or "Please provide the message to be repeated."
#    await ctx.message.delete()
#    await ctx.send(message)
#
#def read_json(filename):
#    with open(f"{cwd}/Config/{filename}.json", "r") as file:
#        data = json.load(file)
#    return data
#
#def write_json(data, filename):
#    with open(f"{cwd}/Config/{filename}.json", "w") as file:
#        json.dump(data, file, indent = 4, sort_keys=True)

bot.run(fichierSecret['token']) # Runs our bot