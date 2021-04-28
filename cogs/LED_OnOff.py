# importing needed libraries
import gpiozero
import discord
import os
import re

#maps GPIO pin to variable. active_high property make it use the 3.3v and GPIO pin
redLED = gpiozero.LED(17, active_high=False)

#event handler for when a message is recieved
@client.event
async def on_message(message):
    #makes sure that the bot isn't responding to itself
    if message.author == client.user:
        return
    else:
        #If the bot is mentioned in the message it will read it.
        if client.user.mentioned_in(message):
            #looks for a regex of "LED on" then sends a message to confirm it has been turned on
            if re.findall(r'\bled on\b', message.content.lower()):
                redLED.on()
                await message.channel.send("The LED has been turned on")
            #looks for a regex of "LED off" then sends a message to confirm it has been turned off
            elif re.findall(r"\bled off\b", message.content.lower()):
                redLED.off()
                await message.channel.send("The LED has been turned off")
            else:
                return
        else:
            return
