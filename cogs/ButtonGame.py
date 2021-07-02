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

    serverID.button datastructure:
    {
        'users':[
                {userID: SilentCinema, score: 1893, timestamp: 1622649960},
                {userID: Panyk, score: 2453, timestamp: 1622649990},
                {userID: Omn1core, score 5435, timestamp: 1622650017}
                ]
        'LastTimestamp': 1622650039
    }
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

    #LeaderboardEmbed()

    #rankEmbed()

    #buttonPressEmbed()

    @commands.group(case_insensitive=True)
    async def button(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid button command passed...')
        pass

    @button.command()
    async def Press(self, ctx):
        #CurrentTimestamp = timestamp
        #open serverID.button as ButtonData
        #scoreList = ButtonData['users']
        #index = next((i for i, item in enumerate(scoreList) if item["userID"] == ctx.UserID), None)
        #scoreList[index]['timestamp']=CurrentTimestamp
        #scoreList[index]['score'] = CurrentTimestamp - ButtonData['lastTimestamp']
        #newlist = sorted(scoreList, key=itemgetter('score'), reverse=True)
        #ButtonData['lastTimestamp'] = CurrentTimestamp
        #ButtonData['users'] = newlist
        #pickle ButtonData to serverID.button
        #close serverID.button
        await ctx.send("Button Press")

    @button.command()
    async def Rank(self, ctx):
        #index = next((i for i, item in enumerate(scoreList) if item["userID"] == ctx.UserID), None)
        #rank = index+1
        await ctx.send("Rank")

    @button.command()
    async def List(self, ctx):
        #ButtonData['users'][range(0,5)]
        await ctx.send("Leaderboard")

def setup(bot):
    bot.add_cog(ButtonGame(bot))
