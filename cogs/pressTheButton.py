#Imports relevant libraries
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
import yaml

# Define a class to manage the points file. Takes in the guild ID as a parameter on creation and makes a file path based on that ID.
class PointsManager:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.file_path = (f"{guild_id}.yaml")

    async def read_points_file(self):
        # Read the points.yaml file to get the last user and their points and return them
        try:
            with open(self.file_path, 'r') as file:
                points_data = yaml.safe_load(file)
                leader_user = points_data.get('leader_user', 'None')
                leader_user_points = points_data.get('points', 0)
        except FileNotFoundError:
            leader_user = "None"
            leader_user_points = 0
        return leader_user, leader_user_points

    async def write_points_file(self, username, points):
        # Update the file with the points for the user and their points
        points_data = {
            'leader_user': username,
            'points': points
        }
        with open(self.file_path, 'w') as file:
            yaml.dump(points_data, file)

class PressTheButton(commands.Cog):
    def __init__(self, discord_client):
        self.discord_client = discord_client
        self.last_pressed = datetime.now()
        self.points_awarded = 0
        self.leader_user = "None"
        self.leader_user_points = 0
        self.last_user = "None"
        self.game_channel = None
        self.MessageID = None
        self.last_embed_update = datetime.now()
        self.points_manager = None

    #Starts the game in the channel where the command was run
    @app_commands.command(name="start_game", description="Start the button game in this channel")
    async def start_game(self, interaction: discord.Interaction):
        if self.update_embed.is_running():
            self.update_embed.stop()
        self.game_channel = interaction.channel
        self.points_manager = PointsManager(interaction.guild_id)
        self.update_embed.start()
        await interaction.response.send_message(f"""Game started! \n 
    How to play: Press the button. \n 
    The point pot resets every time the button is pressed. \n 
    You don't keep points between button presses \n 
    If you have more poitns than the current leader, you will become the new leader.""")
    
    #Stops the game (currently not working has to be fixed)
    @app_commands.command(name="stop_game", description="Stop the button game")
    async def stop_game(self, interaction: discord.Interaction):
        self.update_embed.stop()
        self.MessageID = None
        self.game_channel = None
        await interaction.response.send_message("Game stopped!")

    #View class for the button and controls the logic behind the button
    class ButtonPressView(View):
        def __init__(self, cog):
            super().__init__()
            self.cog = cog

        @discord.ui.button(label="Press Me!", style=discord.ButtonStyle.green)
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Gathers info needed to run logic on the button press
            time_diff = (datetime.now() - self.cog.last_pressed).total_seconds()
            self.cog.points_awarded = int(time_diff)
            self.cog.last_pressed = datetime.now()
            self.cog.last_user = interaction.user.name
            self.cog.leader_user, self.cog.leader_user_points = await self.cog.points_manager.read_points_file()
            
            # Sends a message to the user based on if they beat the current leader or not and runs the logic to update the points
            if self.cog.leader_user_points > self.cog.points_awarded:
                # If the user doesn't beat the current leader, send a message to the user and update the embed of last pressed user
                await interaction.response.send_message(f"You didn't beat {self.cog.leader_user}'s {self.cog.leader_user_points} points. There were only {self.cog.points_awarded} in the pot.", ephemeral=True)
                await self.cog.update_embed()
            else:
                # If the user beats the current leader, send a message to the user and update the points file and renew embed
                await self.cog.points_manager.write_points_file(interaction.user.name, self.cog.points_awarded)
                await interaction.response.send_message(f"Points awarded: {self.cog.points_awarded}", ephemeral=True)
                await self.cog.update_embed(force_new=True)
    
    #Updates the embed
    @tasks.loop(seconds=15)
    async def update_embed(self, force_new=False):
        # Gets the info for the embed
        # Calculate the points awarded and get the current leader info
        time_diff = (datetime.now() - self.last_pressed).total_seconds()
        self.points_awarded = int(time_diff)
        self.leader_user, self.leader_user_points = await self.points_manager.read_points_file()
        
        #creates the embed framework
        embed = discord.Embed(title="The Button Game",
                              description=f"Press the button to claim points! Current points: {self.points_awarded}")
        embed.add_field(name="Current Leader",
                        value=f"{self.leader_user} - {self.leader_user_points} points")
        embed.set_footer(text=f"Last User who pressed the button - {self.last_user}")

        # Logic for creating the embed or editing it
        # Looks for factors that would nessitate a new embed to get around rate limits on editing messages
        # Mainly the embed is recreated when the button is pressed, the last embed update was more than 30 minutes ago, or the message ID is None
        if force_new or (datetime.now() - self.last_embed_update) > timedelta(minutes=30) or self.MessageID is None:
            # Deletes the old message if it exists
            if self.MessageID is not None:
                old_message = await self.game_channel.fetch_message(self.MessageID)
                await old_message.delete()
            
            #creates the embed and updates the last edit time
            message = await self.game_channel.send(embed=embed, view=self.ButtonPressView(self))
            self.MessageID = message.id
            self.last_embed_update = datetime.now()
        # If the embed doesn't need to be recreated, it edits the existing message
        else:
            message = await self.game_channel.fetch_message(self.MessageID)
            await message.edit(embed=embed, view=self.ButtonPressView(self))

async def setup(discord_client: commands.Bot):
    await discord_client.add_cog(PressTheButton(discord_client))