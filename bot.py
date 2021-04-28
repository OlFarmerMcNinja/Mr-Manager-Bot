import os
import discord
from dotenv import load_dotenv

#loading variables from .env which contains auth tokens
load_dotenv()
DISCORD_TOKEN = os.getenv('Discord_Token')
GUILDID = os.getenv('Discord_ServerID')

#starts the discord client
client = discord.Client()


#event handler on start
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, id=int(GUILDID))

    print(
        f'{client.user} has connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
        )

#starts the client and runs the script with the provided token in .env file
client.run(DISCORD_TOKEN)
