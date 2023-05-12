import random
import discord
import database


class dailyVisual(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, item):
        coin_flip = random.randint(1, 2)

        user = database.get_user(interaction.user.id)

        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)

        if coin_flip == 1:
            database.set_money(interaction.user.id, user["balance"] - 100)
            await interaction.response.edit_message(content="for not knowing math i take away 100")
        else:
            database.set_money(interaction.user.id, user["balance"] + 100)
            await interaction.response.edit_message(content="ok enjoy ur 100 coin!!!")

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="so smart!!!")