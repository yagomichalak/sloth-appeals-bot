from lib2to3.pgen2.token import BACKQUOTE
import discord
from discord import slash_command, Webhook
from discord.ext import commands

import os
import aiohttp
from typing import List, Dict
from mysqldb import the_database

from extra import utils
from extra.views import BanAppealsView
from extra.modals import BanAppealModal

guild_ids: List[int] = [int(os.getenv('SERVER_ID'))]
webhook_url: str = os.getenv('WEBHOOK_URL')
slash_command_channel_id: int = int(os.getenv('SLASH_COMMAND_CHANNEL_ID'))

class BanAppeals(commands.Cog):
    """ Category for managing Ban Appeals. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        self.client = client
        self.cache: Dict[int, int] = {}
        self.appeal_cooldown: int = 3600 # In seconds

    # /// Events ///
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """ Tells when the cog is ready to go. """

        self.client.add_view(BanAppealsView(self.client))

        print('BanAppeals cog is ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """ Checks whether people are sending messages in the channel where
        they are only supposed to use Slash commands. """

        if message.channel.id != slash_command_channel_id:
            return

        perms = message.channel.permissions_for(message.author)
        if not perms.administrator:
            await message.delete()

    # /// Commands ///
    @slash_command(name="appeal", guild_ids=guild_ids)
    async def _appeal_slash_command(self, ctx: discord.ApplicationContext) -> None:
        """ Makes a Ban Appeal. """

        member = ctx.author

        # Checks cooldown for making a Ban Appeal (1 hour)
        time_now = await utils.get_timestamp()
        if member_ts := self.cache.get(member.id):
            sub = time_now - member_ts
            if sub <= self.appeal_cooldown:
                return await ctx.respond(
                    f"**You are on cooldown to make your Ban Appeal, try again in {(self.appeal_cooldown-sub)/60:.1f} minutes**", ephemeral=True)

        await ctx.send_modal(BanAppealModal(self.client))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def make_appeals_message(self, ctx) -> None:
        """ Makes the appeal message. """

        guild: discord.Guild = ctx.guild

        embed: discord.Embed = discord.Embed(
            title="**__Ban Appeals__**",
            description="Click on the button below to start making your `Ban Appeal`.",
            color=discord.Color.brand_red()
        )
        embed.set_image(url=guild.icon.url)
        embed.set_author(name=guild.name)
        embed.set_footer(text="Make your appeal!", icon_url=guild.icon.url)
        ban_appeal_view: discord.ui.View = BanAppealsView(self.client)
        await ctx.send(embed=embed, view=ban_appeal_view)

    # /// Methods ///
    async def send_appeal_webhook(self, member: discord.Member, content: str, embed: discord.Embed) -> None:
        """ Sends the Ban Appeal's webhook message to Staff, in The Language Sloth server.
        :param member: The member who made the Ban Appeal.
        :param content: The content of the message.
        :param embed: The embed of the message. """

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, session=session)
            msg = await webhook.send(
                content=content, embeds=[embed], username=member.display_name, avatar_url=member.display_avatar,
                wait=True)
            print(f"• Ban Appeal sent for {member}.")
            # Saves in the database
            await self.insert_ban_appeal(msg.id, member.id, 'ban_appeal')

    async def insert_ban_appeal(self, message_id: int, user_id: int, label: str = "ban_appeal") -> None:
        """ Inserts a Ban Appeal into the database.
        :param message_id: The appeal's message ID.
        :param user_id: The appealer's ID.
        :param label: The label. [Default = ban_appeal] """

        mycursor, db = await the_database()
        await mycursor.execute("""
            INSERT INTO Applications (message_id, applicant_id, application_type)
            VALUES (%s, %s, %s)""", (message_id, user_id, label)
        )
        await db.commit()
        await mycursor.close()

""" To-do List 
----------------------------
    cache [Attribute]
----------------------------
"""

def setup(client: commands.Bot) -> None:
    """ Cog's setup function. """

    client.add_cog(BanAppeals(client))