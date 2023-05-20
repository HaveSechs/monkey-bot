import random

import discord
import database
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def draw_card(name, ability, desc, health, attack, file):
    monkey = Image.open(file).resize((350, 274))
    img = Image.new('RGBA', (500, 750), color='white')

    paste_x = (img.width - monkey.width) // 2
    img.paste(monkey, (paste_x, 0))

    draw = ImageDraw.Draw(img)

    font_32 = ImageFont.truetype("assets/bobby-jones-soft.otf", size=32)
    font_24 = ImageFont.truetype("assets/bobby-jones-soft.otf", size=24)
    center_x = img.width // 2

    draw.text((center_x - draw.textsize(name, font=font_32)[0] // 2, 300), name, fill='black', font=font_32)
    draw.text((center_x - draw.textsize(ability, font=font_32)[0] // 2, 350), ability, fill='black', font=font_32)
    draw.text((center_x - draw.textsize(desc, font=font_24)[0] // 2, 380), desc, fill='black', font=font_24)

    bytes = BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)

    return discord.File(bytes)


class catch(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.clicked = False

    @discord.ui.button(label="catch", style=discord.ButtonStyle.primary)
    async def catch(self, interaction: discord.Interaction, item):
        if not self.clicked:
            self.clicked = True
            user = database.get_user(interaction.user.id)
            if user is None:
                database.new_user(interaction.user.id)
                user = database.get_user(interaction.user.id)

            print(user["pets"] + [self.id])
            database.set_pets(interaction.user.id, user["pets"] + [self.id])
            await interaction.response.edit_message(view=catchDisabled())

            await interaction.channel.send(f"<@{interaction.user.id}> you enslaved it!!!")
        else:
            await interaction.response.send_message("I was already enslaved!!!", ephemeral=True)


class catchDisabled(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="catch", style=discord.ButtonStyle.primary, disabled=True)
    async def catch(self):
        pass


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
                    "type": animal["type"]
                }

        for monkey in range(len(self.deck2)):
            if self.deck2[monkey] is not None:
                animal = database.get_monkey(self.deck2[monkey])
                self.cache[self.user2.id][monkey] = {
                    "health": animal["health"],
                    "attack": animal["attack"],
                    "type": animal["type"]
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

                damage = self.cache[self.turn][self.cache[self.turn]["turns"][-2]]["attack"]
                self.remove_health(self.next, self.cache[self.turn]["turns"][-1], damage)

                if len(self.cache[self.user1.id].keys()) - 1 == 0:
                    await interaction.response.edit_message(content=f"<@{self.user2.id}> won!!!", embed=None, view=None)
                elif len(self.cache[self.user2.id].keys()) - 1 == 0:
                    await interaction.response.edit_message(content=f"<@{self.user1.id}> won!!!", embed=None, view=None)

                await interaction.response.edit_message(embed=self.construct_embed())
                current = self.next
                self.next = self.turn
                self.turn = current

    def remove_health(self, player, slot, amount):
        self.cache[player][slot]["health"] -= amount
        if self.cache[player][slot]["health"] <= 0:
            del self.cache[player][slot]

    def construct_embed(self):
        you = ""
        opp = ""

        for monkey in self.cache[self.user1.id]:
            if monkey != "turns":
                you += f"{self.config['monkey_emojis'][self.cache[self.user1.id][monkey]['type']]} {self.cache[self.user1.id][monkey]['health']} :heart: "

        for monkey in self.cache[self.user2.id]:
            if monkey != "turns":
                opp += f"{self.config['monkey_emojis'][self.cache[self.user2.id][monkey]['type']]} {self.cache[self.user2.id][monkey]['health']} :heart: "

        embed = discord.Embed(title="Fight")
        embed.add_field(name=f"{self.user1.name}", value=you)
        embed.add_field(name=f"{self.user2.name}", value=opp, inline=False)

        return embed