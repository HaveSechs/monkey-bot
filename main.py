import os
import json
import discord
from handles import handles
from utilities import utilities
from dotenv import dotenv_values
from discord.ext import commands
from economy import displays, transactions, monkeys


vals = dotenv_values(".env")


with open("config.json", "r") as f:
    config = json.load(f)

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
