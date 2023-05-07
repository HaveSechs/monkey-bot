import discord
from discord.ext import commands
from discord import app_commands

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