import discord
from discord.ext import commands
from discord import app_commands
import paho.mqtt.client as paho
import yaml
from matplotlib import colors

# Attempt to open and load the configuration file
try:
    with open('Config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
except IOError:
    print("missing config.yaml file, please create one with your bot token in it.")
    exit()

class MQTTPublisher():
    def __init__(self):
        self.mqttClient = paho.Client(config['MQTT_CLIENT_NAME'])
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.connect(config['MQTT_BROKER_IP'], config['MQTT_BROKER_PORT'])
        self.mqttClient.loop_start()
    
    # Callback for when a message is published    
    def on_publish(self, mqtt_client, userdata, mid):
        print("mid: "+str(mid) + " published")
    
    # Publishes the message to the LED sign
    def publish(self, text: str, color: str = None):
        self.mqttClient.publish(config['MQTT_TOPIC'], self.to_yaml(text, color), qos=config['MQTT_QOS'])
    
    # Converts the color to an RGB tuple
    def to_rgb(self, color: str):
        
        # Checks if the color is a valid CSS name, if not it defaults to white
        if color is None:
            hexColor = "#ffffff"
        else:
            try:
                hexColor = colors.CSS4_COLORS[color]
            except KeyError as errorVal:
                hexColor = "#ffffff"
                raise KeyError(f"Color {color} not found. Defaulting to white.") from errorVal
        
        # Takes the hex color and converts it to an RGB tuple
        strippedHex = hexColor.lstrip('#')
        return tuple(int(strippedHex[i:i+2], 16) for i in (0, 2, 4))
    
    # Converts the message information to a YAML payload
    def to_yaml(self, text: str, color: str):
        payload = {
            'text': text[:160],
            'color': self.to_rgb(color)
        }
        return yaml.dump(payload, sort_keys=False)

class SignPublisherCog(commands.Cog, name='signPublisher'):
    def __init__(self, discord_client: commands.Bot):
        super().__init__()
        self.discord_client = discord_client
        self.MQTTPubClient = MQTTPublisher()
        
    @app_commands.command(name='publish', description='Scrolls the given text across the LED matrix.')
    async def scroll_text(self, interaction: discord.Interaction, text: str, color: str = "white"):
        await interaction.response.defer()
            
        #creates the embed
        embed = discord.Embed(
                        title="Done Scrolling Text!",
                        colour=0x00f51d)
        
        embed.set_author(
                        name=interaction.user.name, 
                        icon_url=interaction.user.avatar)

        embed.add_field(name="Your Text:",
                        value=text[:160],
                        inline=False)
        
        # Publishes the message to the LED sign if the color is invalid then
        # it passes it again without the color then adds a warning to the embed
        try:
            self.MQTTPubClient.publish(text[:160], color)
            embed.add_field(name="Color:",
                            value=color,
                            inline=True)
        except KeyError as e:
            self.MQTTPubClient.publish(text[:160])
            embed.add_field(name="Warning:",
                            value="Color not found. Defaulting to white.",
                            inline=True)
        
        #sends the embed
        await interaction.followup.send(embed=embed)

async def setup(discord_client:commands.Bot) -> None:
    await discord_client.add_cog(SignPublisherCog(discord_client))