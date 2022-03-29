import discord
from discord import slash_command, option, Webhook
from discord.ext import commands

from typing import List
import os
import aiohttp

from extra.modals import BanAppealModal

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
webhook_url: str = os.getenv('WEBHOOK_URL')

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

    async def send_appeal_webhook(self, member: discord.Member, content: str, embed: discord.Embed) -> None:
        """ Sends the Ban Appeal's webhook message to Staff, in The Language Sloth server.
        :param member: The member who made the Ban Appeal.
        :param content: The content of the message.
        :param embed: The embed of the message. """


        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, session=session)
            await webhook.send(
                content=content, embeds=[embed], username=member.display_name, avatar_url=member.display_avatar)
            print(f"• Ban Appeal sent for {member}.")


""" To-do List 
----------------------------
    ban_appeal_channel_id
    cosmos_role_id
    insert_application()
    cache =
----------------------------
"""

def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(BanAppeals(client))