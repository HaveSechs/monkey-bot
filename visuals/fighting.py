import discord
import random
import database


class fight(discord.ui.View):
    def __init__(self, turn: int, user1: discord.User, user2: discord.User, config):
        super().__init__()
        self.config = config
        self.special = False

        self.turn = turn

        if user1.id == self.turn:
            self.next = user2.id
        else:
            self.next = user1.id

        self.cache = {
            user1.id: {"turns": []},
            user2.id: {"turns": []}
        }

        deck = database.get_user(user1.id)["deck"]
        for id, pos in enumerate(deck):
            monkey = database.get_monkey(id)
            attributes = self.config["monkey_attributes"][monkey["type"]]
            self.cache[user1.id][pos] = {
                "type": monkey["type"],
                "attack": monkey["attack"],
                "health": monkey["health"],

                "magic": attributes["magic"],
                "magic_only": attributes["magic_only"],
                "black": attributes["black"],
                "extra_turn": attributes["extra_turn"]
            }

        deck = database.get_user(user2.id)["deck"]
        for id, pos in enumerate(deck):
            monkey = database.get_monkey(id)
            attributes = self.config["monkey_attributes"][monkey["type"]]
            self.cache[user2.id][pos] = {
                "type": monkey["type"],
                "attack": monkey["attack"],
                "health": monkey["health"],

                "magic": attributes["magic"],
                "magic_only": attributes["magic_only"],
                "black": attributes["black"],
                "extra_turn": attributes["extra_turn"]
            }

    @discord.ui.button(label="1")
    async def one(self, interaction: discord.Interaction, item):
        await self.attack(interaction, 0)

    @discord.ui.button(label="2")
    async def two(self, interaction: discord.Interaction, item):
        await self.attack(interaction, 1)

    @discord.ui.button(label="3")
    async def three(self, interaction: discord.Interaction, item):
        await self.attack(interaction, 2)

    @discord.ui.button(label="4")
    async def four(self, interaction: discord.Interaction, item):
        await self.attack(interaction, 3)

    @discord.ui.button(label="5")
    async def five(self, interaction: discord.Interaction, item):
        await self.attack(interaction, 4)

    @discord.ui.button(label="Special Ability", style=discord.ButtonStyle.green)
    async def special(self):
        self.special = True

    async def attack(self, interaction, slot):
        if interaction.user.id == self.turn:
            if len(self.cache[self.turn]["turns"]) == 0 or len(self.cache[self.turn]["turns"]) % 2 == 0:
                self.cache[self.turn]["turns"].append(slot)
            else:
                self.cache[self.turn]["turns"].append(slot)

                self.remove_health(self.cache[self.turn]["turns"][-2], self.cache[self.turn]["turns"][-1])
            self.next_turn(self.cache[self.turn]["turns"][-2])

    def remove_health(self, attacker, victim):
        mult = 1
        can = True

        v = self.cache[self.next][victim]
        a = self.cache[self.turn][attacker]

        # multipliers first
        if not a["black"] and v["black"]:
            mult = 10

        # can
        if v["magic_only"] and not a["magic"]:
            can = False

        """
        # specials
        if self.special:
            actual = [
                "kkk monkey"
            ]

            if a["type"] in actual and not a["special_disabled"] and not a["disabled"]:
                if a["type"] == "kkk monkey":
                    self.round_damage.append(
                        [victim, "pct", 0.95]
                    )
                elif a["type"] == "basic monkey":
                    self.cache[self.turn][victim]["extra_turn"] = True

                can = False
        """

        if can:
            self.cache[self.next][victim]["health"] -= a["attack"] * mult

    def next_turn(self, used):
        self.special = False

        if not self.cache[self.turn][used]["extra_turn"]:
            current = self.turn
            self.turn = self.next
            self.next = current
