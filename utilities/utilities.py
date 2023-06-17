import json
import discord
import database
from discord.ext import commands
from discord import app_commands

with open("config.json") as f:
    config = json.load(f)


async def autocomplete_id(interaction: discord.Interaction, id: int):
    print("ok")
    user = database.get_user(interaction.user.id)

    if user is None:
        database.new_user(interaction.user.id)
        user = database.get_user(interaction.user.id)
    print("ok 2")
    choices = []
    print("ok 3")
    print(user)

    for id in user["pets"]:
        print(type(id))
        monkey = database.get_monkey(id)
        print(monkey)

        name = f"{config['monkey_emojis'][monkey['type']]} {monkey['health']} :heart: {monkey['attack']} :dagger:"

        choices.append(
            app_commands.Choice(name=name, value=str(id))
        )
    print(choices)
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