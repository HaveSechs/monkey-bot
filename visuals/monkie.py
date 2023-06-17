import random

import discord
import database
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def draw_card(name, ability, desc, health, attack, file):
    monkey = Image.open(file).resize((350, 274)).convert("RGBA")
    img = Image.new("RGBA", (500, 750), color='blue')

    paste_x = (img.width - monkey.width) // 2
    img.paste(monkey, (paste_x, 0))

    draw = ImageDraw.Draw(img)

    font_48 = ImageFont.truetype("C:\\Users\\ianso\\monkeyBot\\monkey-bot\\assets\\bobby-jones-soft.otf", size=48)
    font_32 = ImageFont.truetype("C:\\Users\\ianso\\monkeyBot\\monkey-bot\\assets\\bobby-jones-soft.otf", size=32)
    font_24 = ImageFont.truetype("C:\\Users\\ianso\\monkeyBot\\monkey-bot\\assets\\bobby-jones-soft.otf", size=24)
    center_x = img.width // 2

    draw.text((center_x - draw.textsize(name, font=font_48)[0] // 2, 300), name, fill='white', font=font_48)
    draw.text((center_x - draw.textsize(ability, font=font_32)[0] // 2, 350), ability, fill='white', font=font_32)
    draw.text((center_x - draw.textsize(desc, font=font_24)[0] // 2, 380), desc, fill='white', font=font_24)

    bytes = BytesIO()
    img.save(bytes, format="PNG")
    bytes.seek(0)

    return discord.File(bytes, filename="monkey.png")


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

            monkey = database.get_monkey(self.id)
            await interaction.channel.send(f"<@{interaction.user.id}> you enslaved it!!!\n\n`{self.id}` **{monkey['health']} :heart: {monkey['attack']} :dagger:**")
        else:
            await interaction.response.send_message("I was already enslaved!!!", ephemeral=True)


class catchDisabled(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="catch", style=discord.ButtonStyle.primary, disabled=True)
    async def catch(self):
        pass


class petsDisplay(discord.ui.View):
    def __init__(self, pages: list, user: discord.User):
        super().__init__()
        self.page = 0
        self.pages = pages
        self.user = user

        self.len_ = 0

        for page in pages:
            self.len_ += len(page)

    @discord.ui.button(label="<")
    async def back(self, interaction: discord.Interaction, item):
        self.page -= 1
        await interaction.response.edit_message(embed=self.construct_embed())

    @discord.ui.button(label=">")
    async def next(self, interaction: discord.Interaction, item):
        self.page += 1
        await interaction.response.edit_message(embed=self.construct_embed())

    def construct_embed(self):
        embed = discord.Embed(title=f"{self.user.name}'s Pets ({self.len_})")
        for monkey in self.pages[self.page]:
            print(monkey)
            animal = database.get_monkey(monkey)
            embed.add_field(name=f"{animal['type']} ({animal['id']})", value=f":heart: {animal['health']} :dagger: {animal['attack']}", inline=False)
        return embed


class tradeDisplay(discord.ui.View):
    def __init__(self, user1, giving, user2, asking):
        super().__init__()
        self.user1 = user1
        self.giving = giving
        self.user2 = user2
        self.asking = asking

        print(giving, asking, user2, user1)

    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, item):
        if interaction.user.id == self.user2:
            print("done")
            user1 = database.get_user(self.user1)
            user2 = database.get_user(self.user2)
            database.remove_from_deck_and_pets(self.user1, self.giving)
            database.remove_from_deck_and_pets(self.user2, self.asking)

            database.set_pets(self.user1, user1["pets"] + [self.asking])
            database.set_pets(self.user2, user2["pets"] + [self.giving])
            await interaction.response.edit_message(content="Trade done!")

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, item):
        if interaction.user.id == self.user2:
            await interaction.response.edit_message(content="Declined", view=None)