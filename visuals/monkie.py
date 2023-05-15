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