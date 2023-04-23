import json
import discord
from discord import app_commands
from discord.ext import commands

from economy import displays
from handles import handles

with open("config.json", "r") as f:
    config = json.load(f)

monkey = commands.Bot(intents=discord.Intents.all(), command_prefix="%")

# displays.setup(monkey)


@monkey.event
async def on_ready():
    await displays.setup(monkey, config)
    await handles.setup(monkey, config)
    await monkey.tree.sync()
    print("""Cercopithecidae
    .-"-. 
  _/_-.-_\_
 ( ( o o ) )
  |/  "  \|
   \ .-. /
   /`\"\"\"`\\
  /       \\""")


monkey.run("")
