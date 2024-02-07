import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Returns the bot's latency in milliseconds.")     
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Pong!", description=f'{round(self.client.latency * 1000)}ms', color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(Ping(client))