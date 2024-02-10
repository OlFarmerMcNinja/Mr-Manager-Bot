import discord
from discord.ext import commands
import yaml
import time
import platform

# Attempt to open and load the configuration file
try:
    with open('Config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
except IOError:
    print("missing config.yaml file, please create one with your bot token in it.")
    exit()

# Creates a timestamp for logging
def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

# Define a new bot class
class DiscordClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.all())
        self.cogslist = config['DISCORD_COGS']
    
    # Loads the cog files
    async def setup_hook(self):
        for ext in self.cogslist:
            try:
                # Attempt to load the cog
                await self.load_extension(ext)
                print(f"Loaded {ext}")
            except Exception as e:
                # If the cog fails to load, print an error message
                print(f"Failed to load {ext}")
                print(e)
    
    # Method called when the bot is ready
    async def on_ready(self):
        # Prints information about the bot
        print(str(getTime()) + " " + "Logged in as " + self.user.name)
        print(str(getTime()) + " " + "ID: " + str(self.user.id))
        print(str(getTime()) + " " + "Discord.py Version: " + discord.__version__)
        print(str(getTime()) + " " + "Python Version: " + platform.python_version())
        
        # Syncs the slash commands and then prints the number of commands synced
        synced = await self.tree.sync()
        print(str(getTime()) + " " + "Tree synced: " + str(len(synced)) + " commands")
    
# creates the bot
discordBot = DiscordClient()

# runs the bot
discordBot.run(config['DISCORD_TOKEN'])