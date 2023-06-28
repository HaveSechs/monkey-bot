import random
import discord
import database
from visuals import monkie


class monkeys:
    def __init__(self, monkey, config):
        self.config = config
        self.monkey = monkey

        self.ftm = {
            "assets/basic.png": "basic monkey",
            "assets/wizard.png": "wizard monkey",
            "assets/ninja.png": "ninja monkey",
            "assets/girl.png": "girl monkey",
            "assets/kkk.png": "kkk monkey",
            "assets/gorilla.png": "gorilla",
            "assets/albino.png": "albino monkey",
            "assets/dj.png": "dj monkey",
            "assets/cyborg.png": "cyborg monkey",
            "assets/soldier.png": "soldier monkey",
            "assets/violent.png": "violent monkey",
            "assets/zombie.png": "zombie monkey"
        }

    def random_monkey(self):
        return random.choices(self.config["chances"]["files"], weights=list(self.config["chances"]["monkeys"].values()), k=1)[0]

    async def spawn(self, channel_id):
        monkey = self.random_monkey()
        channel = self.monkey.get_channel(channel_id)

        await channel.send("Your dad just appeared!", file=discord.File(monkey), view=monkie.catch(database.new_monkey(self.ftm[monkey])))