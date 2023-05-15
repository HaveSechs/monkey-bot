import discord
import database
from discord.ext import commands
from discord import app_commands

import visuals.monkie


class displayEconomy(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config
        # self.tree = app_commands.CommandTree(self.monkey)

    @app_commands.command(name="balance", description="check how broke you are")
    async def balance(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Balance", color=0x336EFF)
        embed.add_field(name="Money", value=f"{user['balance']} :monkey_face:", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="its not about what you have, its about what you don't have")
    async def inventory(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Inventory", color=0x336EFF)

        for item in user["inventory"]:
            embed.add_field(name=f"{item} - {user['inventory'][item]['amount']}", value=self.config["items"][item]["description"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pets", description="nesi is no longer my pet")
    async def pets(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Pets", color=0x336EFF)

        for pet in user["pets"]:
            info = database.get_monkey(pet)
            embed.add_field(name=info["type"] + f" ({info['id']})", value=f":heart: {info['health']} :dagger: {info['attack']}", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="view_pet", description="i have no pets :(")
    async def view_pet(self, interaction: discord.Interaction, pet: int):
        pet = database.get_monkey(pet)
        # card = visuals.monkie.draw_card(pet["type"], self.config["monkey_abilities"][pet["type"]]["ability"], self.config["monkey_abilities"][pet["type"]]["desc"], pet["health"], pet["attack"], f"assets/C{self.config['monkeys'][pet['type']]['asset'].split('/')[1]}")
        # await interaction.response.send_message(file=card)

        # TODO: make it an image
        embed = discord.Embed(title=f"{pet['type']} ({pet['id']})")
        embed.add_field(name=f"Ability: {self.config['monkey_abilities'][pet['type']]['ability']}", value=self.config['monkey_abilities'][pet['type']]['desc'], inline=False)
        embed.add_field(name=f"Health: ", value=f":heart: {pet['health']}")
        embed.add_field(name=f"Attack: ", value=f":dagger: {pet['attack']}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="look at all the things you can't afford")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Shop", color=0x336EFF)

        for item in self.config["shop"].keys():
            shop = self.config["shop"]
            embed.add_field(name=f"{item} - {shop[item]['price']} :monkey_face:", value=self.config["items"][item]["description"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="multipliers", description="boosting ur dumbness")
    async def multipliers(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Multipliers", color=0x336EFF)
        embed.add_field(name="Message", value=f"{self.config['message_multiplier']}", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(monkey, config):
    await monkey.add_cog(displayEconomy(monkey, config))
