import random

import discord
import database
from discord.ext import commands
from discord import app_commands


class handles(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config

    @commands.Cog.listener()
    async def on_message(self, message):
        amount = random.randint(self.config["message_range"][0], self.config["message_range"][1]) * self.config["message_multiplier"]
        print(amount)

        user = database.get_user(message.author.id)
        if user is None:
            database.new_user(message.author.id)
            user = database.get_user(message.author.id)

        database.set_money(message.author.id, user["balance"] + amount)


async def setup(monkey, config):
    await monkey.add_cog(handles(monkey, config))