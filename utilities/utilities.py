import json
import discord
import database
from discord.ext import commands
from discord import app_commands

with open("config.json") as f:
    config = json.load(f)


async def autocomplete_id(interaction: discord.Interaction, id: int):
    user = database.get_user(interaction.user.id)

    if user is None:
        database.new_user(interaction.user.id)
        user = database.get_user(interaction.user.id)

    choices = []

    for id in user["pets"]:
        monkey = database.get_monkey(id)

        name = f"{monkey['type']} 🐵 {monkey['health']} ❤️ {monkey['attack']} 🗡️"

        choices.append(
            app_commands.Choice(name=name, value=str(id))
        )

    return choices


class utilities(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config

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