import os
import platform
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

#loading variables from .env which contains auth tokens
load_dotenv()
DISCORD_TOKEN = os.getenv('Discord_Token')

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
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            extension = file[:-3]
            try:
                bot.load_extension(f'cogs.{extension}')
                print(f'Loaded extension \'{extension}\'')
            except Exception as e:
                exception = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exception}')

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
bot.run(DISCORD_TOKEN)
