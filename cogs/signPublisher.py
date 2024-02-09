import discord
from discord.ext import commands
from discord import app_commands
import paho.mqtt.client as paho

class signPublisherCog(commands.Cog, name='signPublisher'):
    def __init__(self, discord_client: commands.Bot):
        super().__init__()
        self.discord_client = discord_client
        self.mqtt_client = paho.Client("p1")
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.connect('the-mighty-server.local', 1883)
        self.mqtt_client.loop_start()
        
    def on_publish(self, mqtt_client, userdata, mid):
        print("mid: "+str(mid) + " published")
        
    @app_commands.command(name='publish', description='Scrolls the given text across the LED matrix.')
    async def scroll_text(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        
        # Publish the text to the LED sign
        self.mqtt_client.publish('LEDSign/discord', text, qos=1)
        
        #creates the embed
        embed = discord.Embed(
                        title="Done Scrolling Text!",
                        colour=0x00f51d)
        
        embed.set_author(
                        name=interaction.user.name, 
                        icon_url=interaction.user.avatar)

        embed.add_field(name="Your Text:",
                        value=text,
                        inline=False)
        
        #sends the embed
        await interaction.followup.send(embed=embed)

async def setup(discord_client:commands.Bot) -> None:
    await discord_client.add_cog(signPublisherCog(discord_client))