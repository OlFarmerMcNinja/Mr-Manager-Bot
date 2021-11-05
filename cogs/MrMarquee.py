import discord
from discord.ext import commands
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import yaml
import os

with open(os.path.dirname(__file__) + '/../config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

options = RGBMatrixOptions()
options.rows = config['LEDMatrix']['Rows']
options.chain_length = config['LEDMatrix']['Chain']
options.hardware_mapping = config['LEDMatrix']['Hardware']
matrix = RGBMatrix(options = options)
#event handler for when a message is recieved
class Marquee(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Pixel")
    async def Pixel(self, ctx, arg1, arg2, arg3, arg4, arg5):
        matrix.SetPixel(int(arg1), int(arg2), int(arg3), int(arg4), int(arg5))
        await ctx.channel.send(f"You have set pixel at {arg1}, {arg2} to color value {arg3},{arg4},{arg5}")

def setup(bot):
    bot.add_cog(Marquee(bot))
