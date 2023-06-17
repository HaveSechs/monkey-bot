import time
import asyncio
from typing import Literal
import random
import discord
import database
from discord.ext import commands
from discord import app_commands
from visuals import eco
from visuals import monkie
from visuals import fighting
from utilities.utilities import autocomplete_id
import typing

class transactions(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config
        asyncio.ensure_future(self.daily_thread())

    async def daily_thread(self):
        while True:
            if int(time.time()) % 86400 == 0 or int(time.time()) % 86400 == 1:
                database.reset_daily()
            await asyncio.sleep(0.1)

    @app_commands.command(name="daily", description="daily bread and water")
    async def daily(self, interaction: discord.Interaction):
        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(interaction.user.id, 100, False)
        else:
            if user["daily"] is True:
                database.set_money(interaction.user.id, user["balance"] + 100)
                database.set_daily(interaction.user.id, False)
                await interaction.response.send_message("MTA5OTQ4OTM1NTQ5MzU2MDM4Mw.XyPUFE.N77Av8NyNgV4QxXA8qFpSAMspMOo2")
            else:
                await interaction.response.send_message("does 24 hours equal 2 seconds?", view=eco.dailyVisual(interaction.user.id))

    @app_commands.command(name="buy", description="robux robux time !!!!")
    @app_commands.describe(item="you are brokie")
    async def buy(self, interaction: discord.Interaction, item: Literal["100 robux"], amount: int = 1):
        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)

        if user["balance"] >= self.config["shop"][item]["price"] * amount:
            database.set_money(interaction.user.id, user["balance"] - self.config["shop"][item]["price"] * amount)
            try:
                user["inventory"][item]["amount"] += amount
            except:
                user["inventory"][item]["amount"] = amount
            database.set_inventory(interaction.user.id, user["inventory"])
        else:
            await interaction.response.send_message("no money no shit")

    @app_commands.command(name="sell", description="selling black people")
    @app_commands.describe(item="black person")
    async def sell(self, interaction: discord.Interaction, item: Literal["100 robux"], amount: int = 1):
        user = database.get_user(interaction.user.id)

        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)

        if amount <= user["inventory"][item]["amount"]:
            user["inventory"][item]["amount"] -= amount

            if user["inventory"][item]["amount"] == 0:
                del user["inventory"][item]

            database.set_money(interaction.user.id, user["balance"] + amount * self.config["items"][item]["sell_value"])
            database.set_inventory(interaction.user.id, user["inventory"])

            await interaction.response.send_message("Sold!")
        else:
            await interaction.response.send_message("cant count moment")

    @app_commands.command(name="deck_set", description="guts")
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

    @app_commands.command(name="fight", description="one")
    async def fight(self, interaction: discord.Interaction, user: discord.User):
        user1 = database.get_user(interaction.user.id)
        user2 = database.get_user(user.id)
        if user1 is None:
            database.new_user(interaction.user.id)
            user1 = database.get_user(interaction.user.id)

        if user2 is None:
            database.new_user(user.id)
            user2 = database.get_user(user.id)

        if user1["deck"].count(None) == 5 or user2["deck"].count(None) == 5:
            await interaction.response.send_message("one of you guys has no slaves")
        else:

            you = ""
            opp = ""

            cnt = 1

            for monkey in user1["deck"]:
                if monkey is not None:
                    animal = database.get_monkey(monkey)
                    you += f"({cnt}) {self.config['monkey_emojis'][animal['type']]} **{animal['health']} :heart: {animal['attack']} :dagger:**\n"
                    cnt += 1

            cnt = 1

            for monkey in user2["deck"]:
                if monkey is not None:
                    animal = database.get_monkey(monkey)
                    opp += f"({cnt}) {self.config['monkey_emojis'][animal['type']]} **{animal['health']} :heart: {animal['attack']} :dagger:**\n"
                    cnt += 1

            turn = random.choice([interaction.user.id, user.id])

            embed = discord.Embed(title="Battle")
            embed.add_field(name=f"{interaction.user.name}", value=f"{you}")
            embed.add_field(name=f"{user.name}", value=f"{opp}", inline=False)
            await interaction.response.send_message(f"<@{turn}>'s turn", embed=embed, view=fighting.fight(turn, interaction.user, user, self.config))

    @app_commands.command(name="level_up", description="jaws morant")
    # @app_commands.autocomplete(to_level=utilities.autocomplete_id, sacrifice=utilities.autocomplete_id)
    async def level_up(self, interaction: discord.Interaction, to_level: str, sacrifice: str, stat: Literal["attack", "health"]):
        to_level = int(to_level)
        sacrifice = int(sacrifice)

        pet1 = database.get_monkey(to_level)
        pet2 = database.get_monkey(sacrifice)

        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(interaction.user.id)
            database.get_user(interaction.user.id)

        if to_level != sacrifice and to_level in user["pets"] and sacrifice in user["pets"] and pet1["type"] == pet2["type"]:
            database.delete_pet(sacrifice)
            database.remove_from_deck_and_pets(interaction.user.id, sacrifice)
            database.change_pet_stats(to_level, {stat: pet1[stat] + 1})
            await interaction.response.send_message("done")
        else:
            await interaction.response.send_message('`to_level != sacrifice and to_level in user["pets"] and sacrifice in user["pets"] and pet1["type"] == pet2["type"]` make sure it fits this if statement')

    @app_commands.command(name="trade_monkey", description="slave trade")
    # @app_commands.autocomplete(giving=utilities.autocomplete_id)
    async def trade(self, interaction: discord.Interaction, giving: str, asking_user: discord.User, asking: str):
        giving = int(giving)
        asking = int(asking)
        user1 = database.get_user(interaction.user.id)
        user2 = database.get_user(asking_user.id)
        if user1 is None:
            database.new_user(interaction.user.id)
            user1 = database.get_user(interaction.user.id)

        if user2 is None:
            database.new_user(asking_user.id)
            user2 = database.get_user(asking_user.id)

        pet1 = database.get_monkey(asking)
        pet2 = database.get_monkey(giving)

        if giving in user1["pets"] and asking in user2["pets"]:
            print("e")
            await interaction.response.send_message(f"<@{asking_user.id}> would get {giving}\n<@{interaction.user.id}> would get {asking}", view=monkie.tradeDisplay(interaction.user.id, giving, asking_user.id, asking))
        else:
            print("fuck no")

async def setup(monkey, config):
    await monkey.add_cog(transactions(monkey, config))
