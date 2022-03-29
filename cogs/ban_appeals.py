import discord
from discord import slash_command, option
from discord.ext import commands

from typing import List
import os

from extra.modals import BanAppealModal

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]

class BanAppeals(commands.Cog):
    """ Category for managing Ban Appeals. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        self.client = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        print('BanAppeals cog is ready!')

    @slash_command(name="appeal", guild_ids=guild_ids)
    async def _appeal_slash_command(self, ctx: discord.ApplicationContext) -> None:
        """ Makes a Ban Appeal. """

        member: discord.Member = ctx.author

        await ctx.send_modal(BanAppealModal(self.client))
        # await ctx.respond(f"**Here's your `Ban Appeal`, {member.mention}:**")

def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(BanAppeals(client))