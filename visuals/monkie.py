import discord
import database


class catch(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.clicked = False

    @discord.ui.button(label="catch", style=discord.ButtonStyle.primary)
    async def catch(self, interaction: discord.Interaction, item):
        if not self.clicked:
            self.clicked = True
            user = database.get_user(interaction.user.id)
            if user is None:
                database.new_user(interaction.user.id)
                user = database.get_user(interaction.user.id)

            print(user["pets"] + [self.id])
            database.set_pets(interaction.user.id, user["pets"] + [self.id])
            await interaction.response.edit_message(view=catchDisabled())
        else:
            await interaction.response.send_message("I was already enslaved!!!", ephemeral=True)


class catchDisabled(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="catch", style=discord.ButtonStyle.primary, disabled=True)
    async def catch(self):
        pass