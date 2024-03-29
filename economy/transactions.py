import time
import asyncio
import random
import discord
import database
from typing import Literal
from discord.ext import commands
from discord import app_commands
from visuals import eco, monkie, fighting
from utilities.utilities import autocomplete_id


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
                user["inventory"][item] = {"amount": amount}
            database.set_inventory(interaction.user.id, user["inventory"])
        else:
            await interaction.response.send_message("no money no shit")

    @app_commands.command(name="sell", description="selling black people")
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
            await interaction.response.send_message("ok", view=fighting.fight(interaction.user, user, self.config))

    @app_commands.command(name="trade_monkey", description="slave trade")
    @app_commands.autocomplete(giving=autocomplete_id)
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
