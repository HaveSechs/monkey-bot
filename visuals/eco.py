import random
import discord
import database


class dailyVisual(discord.ui.View):
    def __init__(self, original):
        super().__init__()
        self.original = original

    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, item):
        if interaction.user.id == self.original:
            coin_flip = random.randint(1, 2)

            user = database.get_user(interaction.user.id)

            if user is None:
                database.new_user(interaction.user.id)
                user = database.get_user(interaction.user.id)

            if coin_flip == 1:
                database.set_money(interaction.user.id, user["balance"] - 100)
                await interaction.response.edit_message(content="for not knowing math i take away 100", view=dailyVisualDisable())
            else:
                database.set_money(interaction.user.id, user["balance"] + 100)
                await interaction.response.edit_message(content="ok enjoy ur 100 coin!!!", view=dailyVisualDisable())

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, item):
        if interaction.user.id == self.original:
            await interaction.response.edit_message(content="so smart!!!", view=dailyVisualDisable())


class dailyVisualDisable(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="yes", style=discord.ButtonStyle.green, disabled=True)
    async def yes(self):
        pass

    @discord.ui.button(label="no", style=discord.ButtonStyle.red, disabled=True)
    async def no(self):
        pass