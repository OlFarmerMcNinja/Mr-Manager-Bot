import os
import platform
import discord
import yaml
from discord.ext import commands, tasks

#default YAML Document
def CreateNewConfig():
    InstalledCogs = []
    try:
        for file in os.listdir('./cogs'):
            if file.endswith(".py"):
                InstalledCogs.append(file[:-3])
    except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        print(f"Could not get list of cogs \n{exception}")
        os.mkdir("cogs")

    YAMLDefault={'DiscordToken': input("What is your Discord Bot Token?"),
                'Cogs': InstalledCogs}
    with open('config.yaml','w') as file:
        yaml.dump(YAMLDefault, file, default_flow_style=False)

#loading tokens from config file
try:
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
except IOError:
    print("generating config.yaml")
    CreateNewConfig()
    with open('config.yaml','r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


#starts the discord client
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, case_insensitive=True)


#event handler on start
@bot.event
async def on_ready():

    print(
        f'{bot.user} has logged on \n'
        f'Discord.py version: {discord.__version__} \n'
        f'Python version: {platform.python_version()} \n'
        f'Running on: {platform.system()} {platform.release()} ({os.name}) \n'
        '################################'
        )

#loads all cogs from the cogs folder
if __name__ == "__main__":
    for cogName in config['Cogs']:
        try:
            bot.load_extension(f'cogs.{cogName}')
            print(f'Loaded extension \'{cogName}\'')
        except Exception as e:
            exception = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {cogName}\n{exception}')

#event handler that executes when a message is sent
@bot.event
async def on_message(message):
    #ignores the message if the message is from the bot_prefix
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)

#command line feedback when command executedCommand
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Error!",
            description="This command is on %.2fs cool down" % error.retry_after
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(error.missing_perms) + "` to execute this command!"
        )
        await context.send(embed=embed)
    raise error

#starts the client and runs the script with the provided token in .env file
bot.run(config['DiscordToken'])
