import discord
from discord.ui import InputText, Modal
from discord.ext import commands

from .prompt.menu import ConfirmButton
import os

cosmos_role_id: int = int(os.getenv('COSMOS_ROLE_ID'))

class BanAppealModal(Modal):
    """ Class for the Ban Appeal application. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        super().__init__("Ban Appeal")
        self.client = client
        self.cog: commands.Cog = client.get_cog('BanAppeals')

        self.add_item(
            InputText(
                label="Ban Reason",
                placeholder="Why were you banned from The Language Sloth? The reason will be in your messages with the Sloth bot.",
                style=discord.InputTextStyle.paragraph
            )
        )

        self.add_item(
            InputText(
                label="Elaborate the Ban Reason",
                placeholder="Please, elaborate as further as you want the reason why you have been banned.",
                style=discord.InputTextStyle.paragraph
            )
        )
        self.add_item(
            InputText(
                label="I plead.",
                placeholder="Guilty. (I did what I am being accused of.\nNot Guilty. (I did NOT do what I am being accused of.)", 
                style=discord.InputTextStyle.short
            )
        )
        self.add_item(
            InputText(
                label="Additional Notes",
                style=discord.InputTextStyle.paragraph,
                required=False
            )
        )
        self.add_item(
            InputText(
                label="Country of Origin and Gender",# What's your motivation? ",
                placeholder="Tell us where you are originated from, and your gender/pronouns etc.",
                style=discord.InputTextStyle.short, 
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """ Callback for the moderation application. """

        await interaction.response.defer(ephemeral=True)
        member: discord.Member = interaction.user

        embed = discord.Embed(
            title=f"__Ban Appeal__",
            color=member.color
        )

        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Question 1", value=self.children[0].value, inline=False)
        embed.add_field(name="Question 2", value=self.children[1].value, inline=False)
        embed.add_field(name="Question 3", value=self.children[2].value, inline=False)
        embed.add_field(name="Question 4", value=self.children[3].value, inline=False)
        embed.add_field(name="Question 5", value=self.children[4].value, inline=False)

        confirm_view = ConfirmButton(member, timeout=60)

        await interaction.followup.send(
            content="Are you sure you want to send this appeal?",
            embed=embed, view=confirm_view, ephemeral=True)

        await confirm_view.wait()
        if confirm_view.value is None: # Timeout
            return await confirm_view.interaction.followup.send(f"**{member.mention}, you took too long to answer...**", ephemeral=True)

        if not confirm_view.value: # Declined
            self.cog.cache[member.id] = 0
            return await confirm_view.interaction.followup.send(f"**Not doing it then, {member.mention}!**", ephemeral=True)

        # Confirmed
        await confirm_view.interaction.followup.send(
            content="**• Ban Appeal successfully made and sent to the Staff, please, be patient now.**", ephemeral=True)

        await self.cog.send_appeal_webhook(member=member, content=f"<@&{cosmos_role_id}>, {member.mention}", embed=embed)
        # Saves in the database
        # await self.cog.insert_application(app.id, member.id, 'ban_appeal')