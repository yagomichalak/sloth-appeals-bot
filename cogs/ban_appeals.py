import discord
from discord import slash_command, option
from discord.ext import commands

class BanAppeals(commands.Cog):
    """ Category for managing Ban Appeals. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('BanAppeals cog is ready!')

def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(BanAppeals(client))