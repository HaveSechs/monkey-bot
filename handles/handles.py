import re
import random
import discord
import database
from discord.ext import commands
from discord import app_commands


class handles(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config
        self.invites = None

    """
    @commands.Cog.listener()
    async def on_ready(self):
        # you can make this bot for multiple servers if you want but I made it only for mine
        target = self.monkey.get_guild(self.config["guild"])
        self.invites = await target.invites()
    """
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.send("**5 invites = Free Admin**\n\nAnyways meet some nigers while ur here")
        except:
            print(f"Could not dm {member.name}")

        target = self.monkey.get_guild(self.config["guild"])
        invites = await target.invites()

        # for invite in invites:

    @commands.Cog.listener()
    async def on_message(self, message):
        amount = random.randint(self.config["message_range"][0], self.config["message_range"][1]) * self.config["message_multiplier"]
        # print(amount)

        user = database.get_user(message.author.id)
        if user is None:
            database.new_user(message.author.id)
            user = database.get_user(message.author.id)

        database.set_money(message.author.id, user["balance"] + amount)

        if message.author.id == 302050872383242240:
            user = database.get_user(message.interaction.user.id)
            if user is None:
                database.new_user(message.author.id, 500)
            else:
                database.set_money(message.interaction.user.id, user["balance"] + 500)
            await message.channel.send("Added 500!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != self.monkey.user.id and len(message.content) != 0:
            content = re.sub("@everyone", "", message.content)
            await message.channel.send(f"""# \"{content}\"
    

# -<@{message.author.id}>""")


async def setup(monkey, config):
    await monkey.add_cog(handles(monkey, config))
