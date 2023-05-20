import discord
from discord.ext import commands
from discord import app_commands

import database


class utilities(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config

    async def autocomplete_id(self, interaction: discord.Interaction, id: int):
        user = database.get_user(interaction.user.id)

        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)
        return [
            app_commands.Choice(name=monkey, value=monkey)
            for monkey in user["pets"] if str(id) in str(monkey)
        ]

    @app_commands.command(name="suggest", description="random")
    async def suggest(self, interaction: discord.Interaction, sentence: str):
        if len(sentence.split()) < 3:
            await interaction.response.send_message("too short bozo")
        else:
            with open("suggestions.txt", "a") as f:
                f.write(sentence + "\n")

            await interaction.response.send_message("done")


async def setup(monkey, config):
    await monkey.add_cog(utilities(monkey, config))