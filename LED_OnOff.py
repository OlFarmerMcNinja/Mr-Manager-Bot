import gpiozero
import discord
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('Discord_Token')
GUILD = os.getenv('Discord_Server')
GUILDID = os.getenv('Discord_ServerID')

client = discord.Client()
red = gpiozero.LED(17, active_high=False)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, id=int(GUILDID))
    
    print(
        f'{client.user} has connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
        )
    
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    else:
        if client.user.mentioned_in(message):
            print("That's me!")
            print(message.content)
            if re.findall(r'\bled on\b', message.content.lower()):
                await message.channel.send("The LED has been turned on")
                red.on()
                print("LED on")
            elif re.findall(r"\bled off\b", message.content.lower()):
                await message.channel.send("The LED has been turned off")
                red.off()
                print("LED off")
            else:
                return
        else:
            return

client.run(TOKEN)