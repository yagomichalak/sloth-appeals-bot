import discord
from discord.ext import commands
from . import utils
from .modals import BanAppealModal

class BanAppealsView(discord.ui.View):
    """ View for the Ban Appeals. """

    def __init__(self, client: commands.Bot) -> None:
        """ Class init method. """

        super().__init__(timeout=None)
        self.client = client
        self.cog = client.get_cog('BanAppeals')

    @discord.ui.button(label="Make Ban Appeal!", style=discord.ButtonStyle.danger, custom_id=f"ban_appeal_id", emoji="<:politehammer:608941633454735360>")
    async def make_ban_appeal_button(self, button: discord.ui.button, interaction: discord.Interaction) -> None:
        """ Button for making a ban appeal. """

        member = interaction.user

        # Checks cooldown for making a Ban Appeal (1 hour)
        time_now = await utils.get_timestamp()
        if member_ts := self.cog.cache.get(member.id):
            sub = time_now - member_ts
            if sub <= self.cog.appeal_cooldown:
                return await interaction.response.send_message(
                    f"**You are on cooldown to make your Ban Appeal, try again in {(self.appeal_cooldown-sub)/60:.1f} minutes**", ephemeral=True)

        await interaction.response.send_modal(BanAppealModal(self.client))
