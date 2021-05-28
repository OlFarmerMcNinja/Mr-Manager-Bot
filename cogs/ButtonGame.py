import datetime
import discord
from discord.ext import commands

class ButtonGame(commands.Cog):
    """
    - Players can use this command to press a button.
    - When the button is pressed then a timestamp is recorded and attached to
    the user who pressed the button.
    - A leaderboard is made that can be invoked via a subcommand (list) that lists
    the top five longest timestamps and the player who pressed it.
    - Players can see their rank among everyone on the servervia the rank
    subcommand.
    """

    def __init__(self, bot):
        self.bot = bot
        self.last_timestamp = None
        self.PlayerData = None

    #creates a file with the serverID as a name to store player data into
    #if <serverID from message>.dat doesn't exist:
        #create <serverID from message>.dat
    #else:
        #open .dat file and save to PlayerData variable
        #last_timestamp = last timestamp from .dat file

    @commands.group(case_insensitive=True)
    async def button(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid button command passed...')
        pass

    @button.command()
    async def Press(self, ctx):
        #CurrentTimestamp = timestamp
        await ctx.send("Button Press")

    @button.command()
    async def Rank(self, ctx):
        await ctx.send("Rank")

    @button.command()
    async def List(self, ctx):
        await ctx.send("Leaderboard")

def setup(bot):
    bot.add_cog(ButtonGame(bot))
