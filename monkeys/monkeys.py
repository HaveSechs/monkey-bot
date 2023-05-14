import discord

class monkeys:
    def __init__(self, monkey):
        self.monkey = monkey

    async def spawn(self, channel_id):
        channel = self.monkey.get_channel(channel_id)
        await channel.send("test")