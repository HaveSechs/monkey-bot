import time
import asyncio
from typing import Literal

import discord
import database
from discord.ext import commands
from discord import app_commands


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
            print(user)
            if user["daily"] is True:
                database.set_money(interaction.user.id, user["balance"] + 100)
                database.set_daily(interaction.user.id, False)
                await interaction.response.send_message("MTA5OTQ4OTM1NTQ5MzU2MDM4Mw.XyPUFE.N77Av8NyNgV4QxXA8qFpSAMspMOo2")
            else:
                await interaction.response.send_message("does 24 hours equal 2 seconds?")

    @app_commands.command(name="buy", description="robux robux time !!!!")
    @app_commands.describe(item="you are brokie")
    async def buy(self, interaction: discord.Interaction, item: Literal["100 robux"]):
        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(interaction.user.id)
            await interaction.response.send_message("too broke")
        else:
            if user["balance"] >= self.config["shop"][item]["price"]:
                database.set_money(interaction.user.id, user["balance"] - self.config["shop"][item]["price"])
                try:
                    user["inventory"][item] += 1
                except:
                    user["inventory"][item] = 1
                database.set_inventory(interaction.user.id, user["inventory"])
            else:
                await interaction.response.send_message("no money no shit")


async def setup(monkey, config):
    await monkey.add_cog(transactions(monkey, config))
