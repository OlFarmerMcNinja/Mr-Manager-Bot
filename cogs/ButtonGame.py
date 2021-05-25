import datetime
import discord
from discord importing commands

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

    @commands.group(case_insensitive=True)
    async def Button(self, ctx):
        pass

    @Button.command()
    async def Press(ctx):
        pass

    @Button.command()
    async def Rank(ctx):
        pass

    @Button.command()
    async def List(ctx):
        pass

def setup(bot):
    bot.add_cog(ButtonGame(bot))
