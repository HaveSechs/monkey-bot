import random
import database
import threading
from utilities.utilities import *
from monkeys import monkeys
from discord.ext import commands


class handles(commands.Cog):
    def __init__(self, monkey, config):
        self.monkeys = monkeys.monkeys(monkey, config)
        self.monkey = monkey
        self.config = config
        self.invites = None
        self.chance = 0
        self.cache = {}
        self.queue = []

        asyncio.ensure_future(self.racism_thread())

    async def racism_thread(self):
        while True:
            if len(self.queue) != 0:
                channel = await self.monkey.fetch_channel(self.queue[0]["cid"])
                message = await channel.fetch_message(self.queue[0]["id"])

                await message.reply("# :warning: remember we do not tolerate racism in this server")

                self.queue.pop(0)
            await asyncio.sleep(0.1)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await member.send("# 1 invite = Free Admin\n\nAnyways meet some nigers while ur here")
        except:
            print(f"Could not dm {member.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and not message.author.bot and len(message.content) > 1:
            # threading.Thread(target=utilities.is_racist, args=(message, self.queue)).start()
            if message.guild.id not in self.cache:
                self.cache[message.guild.id] = {"chance": 0, "time": 0}

            if int(time.time()) - self.cache[message.guild.id]["time"] >= 200:
                self.cache[message.guild.id]["chance"] += 1

                if random.randint(1, 150) <= self.cache[message.guild.id]["chance"]:
                    await self.monkeys.spawn(message.channel.id)
                    self.cache[message.guild.id]["time"] = int(time.time())
                    self.cache[message.guild.id]["chance"] = 0

            await do_quests(message)
            await random_message(message)
            await message_rewards(message)
            await handle_disboard(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != self.monkey.user.id and len(message.content) != 0:
            content = re.sub("@everyone", "", message.content)
            await message.channel.send(f"""# \"{content}\"
    
# -<@{message.author.id}>""")


async def setup(monkey, config):
    await monkey.add_cog(handles(monkey, config))
