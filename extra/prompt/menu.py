import discord
from typing import Union, Optional

class ConfirmButton(discord.ui.View):
    """ View for a prompting confirmation to the user. """

    def __init__(self, member: Union[discord.User, discord.Member], timeout: int = 180) -> None:
        """ Class init method. """

        super().__init__(timeout=timeout)
        self.member = member
        self.value = None
        self.interaction: Optional[discord.Interaction] = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """ Confirms the prompt. """

        self.value = True
        self.interaction = interaction
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """ Declines the prompt. """

        self.value = False
        self.interaction = interaction
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """ Checks whether the person who interacted with the prompt is the one who started it. """

        return self.member.id == interaction.user.id

