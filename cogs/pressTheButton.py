#Imports relevant libraries
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
from discord import app_commands
from datetime import datetime
import asyncio
import yaml

class PressTheButton(commands.Cog):
    def __init__(self, discord_client):
        self.discord_client = discord_client
        self.last_pressed = datetime.now()
        self.points_awarded = 0
        self.leader_user = "None"
        self.last_user = "None"
        self.game_channel = None
        self.MessageID = None

    @app_commands.command(name="start_game", description="Start the button game in this channel")
    async def start_game(self, interaction: discord.Interaction):
        if self.update_embed.is_running():
            self.update_embed.stop()
            self.game_channel = None
            self.MessageID = None
        self.game_channel = interaction.channel
        self.update_embed.start()

    class ButtonPressView(View):
        def __init__(self, cog):
            super().__init__()
            self.cog = cog

        @discord.ui.button(label="Press Me!", style=discord.ButtonStyle.green)
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            time_diff = (datetime.now() - self.cog.last_pressed).total_seconds()
            self.cog.points_awarded = int(time_diff)
            self.cog.last_pressed = datetime.now()
            self.cog.last_user = interaction.user.name
            self.cog.leader_user, self.cog.leader_user_points = await self.cog.read_points_file()
            if self.cog.leader_user_points > self.cog.points_awarded:
                await interaction.response.send_message(f"You didn't beat {self.cog.leader_user}'s {self.cog.leader_user_points} points. There were only {self.cog.points_awarded} in the pot.", ephemeral=True)
                await self.cog.update_embed()
            else:
                await self.update_points_file(interaction.user.name, self.cog.points_awarded)
                await interaction.response.send_message(f"Points awarded: {self.cog.points_awarded}", ephemeral=True)
                await self.cog.update_embed()

        async def update_points_file(self, username, points):
            # Update the file with the points for the last person who pressed the button
            points_data = {
            'leader_user': username,
            'points': points
            }

            with open('points.yaml', 'w') as file:
                yaml.dump(points_data, file)

    @app_commands.command(name="stop_game", description="Stop the button game")
    async def stop_game(self, interaction: discord.Interaction):
        self.update_embed.stop()
        self.MessageID = None
        self.game_channel = None
        await interaction.response.send_message("Game stopped!")

    async def read_points_file(self):
        # Read the points.yaml file to get the last user and their points
        try:
            with open('points.yaml', 'r') as file:
                points_data = yaml.safe_load(file)
                leader_user = points_data.get('leader_user', 'None')
                leader_user_points = points_data.get('points', 0)
        except FileNotFoundError:
            leader_user = "None"
            leader_user_points = 0
        return leader_user, leader_user_points
        

    @tasks.loop(seconds=8)
    async def update_embed(self):
        if not self.game_channel:
            print("No game channel set, run /start_game.")
            return
        time_diff = (datetime.now() - self.last_pressed).total_seconds()
        self.points_awarded = int(time_diff)
        self.leader_user, self.leader_user_points = await self.read_points_file()
        embed = discord.Embed(title="The Button Game",
                      description=f"Press the button to claim points! Current points: {self.points_awarded}")
        embed.add_field(name="Current Leader",
                        value=f"{self.leader_user} - {self.leader_user_points} points")
        embed.set_footer(text=f"Last User who pressed the button - {self.last_user}")
        if self.MessageID is None:
            message = await self.game_channel.send(embed=embed, view=self.ButtonPressView(self))
            self.MessageID = message.id
        else:
            message = await self.game_channel.fetch_message(self.MessageID)
            await message.edit(embed=embed, view=self.ButtonPressView(self))

async def setup(discord_client: commands.Bot):
    await discord_client.add_cog(PressTheButton(discord_client))