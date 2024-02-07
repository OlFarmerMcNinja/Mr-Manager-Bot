
from discord.ext import commands
from discord import app_commands
import discord
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

class ScrollingTextCog(commands.Cog, name='scroll'):
    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client
        
        
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 3
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        self.matrix = RGBMatrix(options = options)
    
    async def scrolling_text(self, text: str):
        self.matrix.Clear()
        
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = canvas.width
        
        while pos + len(text) * 7 > 0:
            canvas.Clear()
            length = graphics.DrawText(canvas, font, pos, 10, textColor, text)
            pos -= 1.25
            time.sleep(0.05)
            canvas = self.matrix.SwapOnVSync(canvas)
        
    @app_commands.command(name='text', description='Scrolls the given text across the LED matrix.')
    async def scroll_text(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer(ephemeral=True)
        
        await self.scrolling_text(text)
        
        await interaction.followup.send("Done scrolling text!", ephemeral=True)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(ScrollingTextCog(client))