
from discord.ext import commands
from discord import app_commands
import discord
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

class ScrollingTextCog(commands.Cog, name='sign'):
    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client
        
        # Set up the LED matrix properties
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 3
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        self.matrix = RGBMatrix(options = options)
    
    async def scrolling_text(self, text: str):
        self.matrix.Clear()
        
        #creates the canvas and loads the text properties
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = canvas.width
        
        # Loop through rendering the text
        while pos + len(text) * 7 > 0:
            canvas.Clear()
            length = graphics.DrawText(canvas, font, pos, 10, textColor, text)
            pos -= 1 # Move left change for speed
            time.sleep(0.05) # scroll smoothness
            canvas = self.matrix.SwapOnVSync(canvas)
    
    # Command to scroll text
    @app_commands.command(name='sign', description='Scrolls the given text across the LED matrix.')
    async def scroll_text(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        
        await self.scrolling_text(text)
        
        #creates the embed
        embed = discord.Embed(title="Done Scrolling Text!",
                      colour=0x00f51d)
        
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)

        embed.add_field(name="Your Text:",
                        value=text,
                        inline=False)
        
        #sends the embed
        await interaction.followup.send(embed=embed)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(ScrollingTextCog(client))