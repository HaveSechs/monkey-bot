import discord
import database
import visuals
from typing import Literal
from discord.ext import commands
from discord import app_commands
from utilities.utilities import autocomplete_id


class monkeys(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config

    view = app_commands.Group(name="view", description="idk")
    deck = app_commands.Group(name="deck", description="idk")

    @view.command(name="pet", description="view your slave")
    @app_commands.autocomplete(pet=autocomplete_id)
    async def view_pet(self, interaction: discord.Interaction, pet: str):
        pet = int(pet)
        pet = database.get_monkey(pet)
        card = visuals.monkie.draw_card("Violent Monkey", "AK-47", "Can attack twice in same turn", 100, 100, "C:\\Users\\ianso\\monkeyBot\\monkey-bot\\assets\\ok.png")
        await interaction.response.send_message(file=card)

    @view.command(name="deck", description="look at ur best slaves")
    async def view_deck(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user.id

        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(who)
            user = database.get_user(who)

        embed = discord.Embed(title="Deck", color=0x336EFF)
        for monkey in user["deck"]:
            if monkey is not None:
                real = database.get_monkey(monkey)
                embed.add_field(name=f"{self.config['monkey_emojis'][real['type']]} ({monkey})", value=f":heart: {real['health']} :dagger: {real['attack']}", inline=True)
            else:
                embed.add_field(name="Empty", value=":heart: 0 :dagger: 0", inline=True)

        await interaction.response.send_message(embed=embed)

    @deck.command(name="set", description="your benched")
    @app_commands.autocomplete(id=autocomplete_id)
    async def deck_set(self, interaction: discord.Interaction, id: str, slot: Literal[1, 2, 3, 4, 5]):
        id = int(id)
        user = database.get_user(interaction.user.id)

        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)

        if id not in user["pets"]:
            await interaction.response.send_message("non existent slave moment", ephemeral=True)
        else:
            if id not in user["deck"]:
                database.set_deck(interaction.user.id, slot - 1, id)
                await interaction.response.send_message("ok")


async def setup(monkey, config):
    await monkey.add_cog(monkeys(monkey, config))