# importing needed libraries
import gpiozero
import discord
from discord.ext import commands

#maps GPIO pin to variable. active_high property make it use the 3.3v and GPIO pin
redLED = gpiozero.LED(17, active_high=False)

#event handler for when a message is recieved
class IoTController(commands.Cog):
    """This command controls all Internet of Things devices connected
    to the raspberry Pi that the bot is running on."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="LED")
    async def LED(self, ctx, arg):
        #if the argument provided is "On" then it will turn the LED on
        if arg.lower() == "on":
            redLED.on()
            await ctx.channel.send("The LED has been turned on")
        #if the argument provided is "Off" then it will turn the LED off
        elif arg.lower() == "off":
            redLED.off()
            await ctx.channel.send("The LED has been turned off")
        else:
            await ctx.channel.send("Please only tell me to turn the LED on or off.")

def setup(bot):
    bot.add_cog(IoTController(bot))
