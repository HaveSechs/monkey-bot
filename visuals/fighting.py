import discord
import random
import database


class fight(discord.ui.View):
    def __init__(self, user1: discord.User, user2: discord.User, config):
        super().__init__()
        self.config = config
        self.turn = random.choice([user1.id, user2.id])
        if self.turn == user1.id:
            self.next = user2.id
        else:
            self.next = user1.id
        self.user1 = user1
        self.user2 = user2
        self.cache = {
            self.user1.id: {"turns": []},
            self.user2.id: {"turns": []}
        }

        self.deck1 = database.get_user(user1.id)["deck"]
        self.deck2 = database.get_user(user2.id)["deck"]

        for monkey in range(len(self.deck1)):
            if self.deck1[monkey] is not None:
                animal = database.get_monkey(self.deck1[monkey])
                self.cache[self.user1.id][monkey] = {
                    "health": animal["health"],
                    "attack": animal["attack"],
                    "type": animal["type"],
                    "extra_turn": False
                }

        for monkey in range(len(self.deck2)):
            if self.deck2[monkey] is not None:
                animal = database.get_monkey(self.deck2[monkey])
                self.cache[self.user2.id][monkey] = {
                    "health": animal["health"],
                    "attack": animal["attack"],
                    "type": animal["type"],
                    "extra_turn": False
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

    async def attack(self, interaction: discord.Interaction, slot):
        if self.turn != interaction.user.id:
            await interaction.response.send_message("not ur turn", ephemeral=True)
        else:
            if len(self.cache[self.turn]["turns"]) == 0 or len(self.cache[self.turn]["turns"]) % 2 == 0: # first time
                self.cache[self.turn]["turns"].append(slot)
                await interaction.response.send_message("Now pick someone to attack", ephemeral=True)

            else:
                self.cache[self.turn]["turns"].append(slot)
                print(self.cache[self.turn])
                damage = self.cache[self.turn][self.cache[self.turn]["turns"][-2]]["attack"]
                self.remove_health(self.next, self.cache[self.turn]["turns"][-1], damage)

                if len(self.cache[self.user1.id].keys()) - 1 == 0:
                    await interaction.response.edit_message(content=f"<@{self.user2.id}> won!!!", embed=None, view=None)
                elif len(self.cache[self.user2.id].keys()) - 1 == 0:
                    await interaction.response.edit_message(content=f"<@{self.user1.id}> won!!!", embed=None, view=None)

                self.next_turn()
                await interaction.response.edit_message(content=f"<@{self.turn}>'s turn", embed=self.construct_embed())

    def next_turn(self):
        if len(self.cache[self.turn]["turns"]) - len(self.cache[self.next]["turns"]) == 4:
            current = self.next
            self.next = self.turn
            self.turn = current
        else:
            used = self.cache[self.turn]["turns"][-2]
            if self.cache[self.turn][used]["type"] not in self.config["default_extra_turns"]:
                current = self.next
                self.next = self.turn
                self.turn = current

    def remove_health(self, player, slot, amount, attacker_type):
        can = True
        if self.cache[player][slot]["type"] in self.config["magic_only"]:
            if attacker_type not in self.config["magic_monkeys"]:
                can = False

        if can:
            self.cache[player][slot]["health"] -= amount
            if self.cache[player][slot]["health"] <= 0:
                del self.cache[player][slot]

    def construct_embed(self):
        you = ""
        opp = ""

        for monkey in self.cache[self.user1.id]:
            if monkey != "turns":
                you += f"({monkey + 1}) {self.config['monkey_emojis'][self.cache[self.user1.id][monkey]['type']]} **{self.cache[self.user1.id][monkey]['health']} :heart: {self.cache[self.user1.id][monkey]['attack']} :dagger:**\n"

        for monkey in self.cache[self.user2.id]:
            if monkey != "turns":
                opp += f"({monkey + 1}) {self.config['monkey_emojis'][self.cache[self.user2.id][monkey]['type']]} **{self.cache[self.user2.id][monkey]['health']} :heart: {self.cache[self.user2.id][monkey]['attack']} :dagger:**\n"

        embed = discord.Embed(title="Fight")
        embed.add_field(name=f"{self.user1.name}", value=you)
        embed.add_field(name=f"{self.user2.name}", value=opp, inline=False)

        return embed