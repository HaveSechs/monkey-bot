import discord
import random
import database


class fight(discord.ui.View):
    def __init__(self, user1, user2, config):
        super().__init__()

        user1_info = database.get_user(user1.id)
        user2_info = database.get_user(user2.id)

        self.user1 = user1
        self.user2 = user2

        self.config = config

        self.cache = {
            user1.id: {
                "started": None, # will do later
                "turns": [],
                "deck": self.load_deck(user1_info["deck"]),
            },
            user2.id: {
                "started": None, # will do later
                "turns": [],
                "deck": self.load_deck(user2_info["deck"])
            }
        }

    @discord.ui.button(label="1")
    async def one(self, interaction: discord.Interaction, item):
        await self.attack(interaction.user.id, 0)
        await interaction.response.edit_message(embed=self.construct_embed())

    @discord.ui.button(label="2")
    async def two(self, interaction: discord.Interaction, item):
        await self.attack(interaction.user.id, 1)
        await interaction.response.edit_message(embed=self.construct_embed())

    @discord.ui.button(label="3")
    async def three(self, interaction: discord.Interaction, item):
        await self.attack(interaction.user.id, 2)
        await interaction.response.edit_message(embed=self.construct_embed())

    @discord.ui.button(label="4")
    async def four(self, interaction: discord.Interaction, item):
        await self.attack(interaction.user.id, 3)
        await interaction.response.edit_message(embed=self.construct_embed())

    @discord.ui.button(label="5")
    async def five(self, interaction: discord.Interaction, item):
        await self.attack(interaction.user.id, 4)
        await interaction.response.edit_message(embed=self.construct_embed())

    async def attack(self, turn: int, used: int):  # turn is the user that clicked and used is the button they selected
        if (len(self.cache[turn]["turns"]) + 1) % 2 == 0 and len(self.cache[turn]["turns"]) > 0:  # this is who to attack
            self.cache[turn]["turns"].append(used)

            not_turn = self.user1.id if turn == self.user2 else self.user2.id

            attacker = self.cache[turn]["deck"][self.cache[turn]["turns"][-2]]
            victim = self.cache[not_turn]["deck"][self.cache[turn]["turns"][-1]]

            if not attacker["attributes"]["disabled"]:
                # boost = self.add_boosters(attacker, victim)
                boost = 1

                self.cache[not_turn]["deck"][self.cache[turn]["turns"][-1]]["health"] -= boost * attacker["attack"]

                if self.cache[not_turn]["deck"][self.cache[turn]["turns"][-1]]["health"] <= 0:
                    self.cache[not_turn]["deck"].pop(self.cache[turn]["turns"][-1])


        else:  # select who is the attacker
            self.cache[turn]["turns"].append(used)

    def load_deck(self, deck):
        new_deck = []
        for monkey in deck:
            if monkey is not None:
                monkey = database.get_monkey(monkey)
                new_deck.append({
                    "type": monkey["type"],
                    "health": monkey["health"],
                    "attack": monkey["attack"],
                    "attributes": self.config["monkey_attributes"][monkey["type"]]
                })
        return new_deck

    def construct_embed(self):
        embed = discord.Embed(title="Battle")

        monkeys = ""

        for pos, monkey in enumerate(self.cache[self.user1.id]["deck"]):
            monkeys += f"({pos + 1}) **{monkey['type']}** {monkey['health']} :heart: {monkey['attack']} :dagger:\n"

        embed.add_field(name=self.user1.name, value=monkeys)

        monkeys = ""

        for pos, monkey in enumerate(self.cache[self.user2.id]["deck"]):
            monkeys += f"({pos + 1}) **{monkey['type']}** {monkey['health']} :heart: {monkey['attack']} :dagger:\n"

        embed.add_field(name=self.user2.name, value=monkeys)
        embed.add_field(name="Dev debug", value=f"`{self.cache[self.user1.id]}`")

        return embed