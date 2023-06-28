import os
import json
import discord
from handles import handles
from utilities import utilities
from dotenv import dotenv_values
from discord.ext import commands
from economy import displays, transactions, monkeys


vals = dotenv_values(".env")


def check_config(config):
    monkey_chances = config["chances"]["monkeys"]
    monkey_files = config["chances"]["files"]
    monkey_abilities = config["monkey_abilities"]
    monkey_emojis = config["monkey_emojis"]
    monkey_attributes = config["monkey_attributes"]

    if len(monkey_files) != len(monkey_chances):
        raise Exception("One of them are missing a monkey")

    for name in monkey_chances:
        if name not in monkey_abilities:
            raise Exception(f"abilities missing {name}")
        if name not in monkey_emojis:
            raise Exception(f"emojis missing {name}")
        if name not in monkey_attributes:
            raise Exception(f"attributes missing {name}")


with open("config.json", "r") as f:
    config = json.load(f)
    check_config(config)

monkey = commands.Bot(intents=discord.Intents.all(), command_prefix="%")


@monkey.event
async def on_ready():
    await monkey.change_presence(activity=discord.Game("With Children"))
    await displays.setup(monkey, config)
    await handles.setup(monkey, config)
    await transactions.setup(monkey, config)
    await utilities.setup(monkey, config)
    await monkeys.setup(monkey, config)
    await monkey.tree.sync()
    print("""Cercopithecidae
    .-"-. 
  _/_-.-_\_
 ( ( o o ) )
  |/  "  \|
   \ .-. /
   /`\"\"\"`\\
  /       \\""")


monkey.run(vals["TOKEN"])
