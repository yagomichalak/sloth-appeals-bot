import discord
from discord.ui import InputText, Modal
from discord.ext import commands
# from .prompt.menu import ConfirmButton
import asyncio

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
        await interaction.followup.send("**Ban Appeal successfully sent!**", ephemeral=True)