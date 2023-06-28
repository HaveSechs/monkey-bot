import re
import discord


def get_link(url):
    url = url.split("http://")
    return "http://" + url[-1]


class torLinks(discord.ui.View):
    def __init__(self, links, id: int):
        super().__init__()
        self.links = links
        self.pos = 1
        self.user_id = id

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def back(self, interaction: discord.Interaction, item):
        if self.pos - 1 >= 0 and interaction.user.id == self.user_id:
            self.pos -= 1

            msg = ""
            for res in self.links[self.pos * 10:(self.pos + 1) * 10]:
                link = res.find("a")
                title = re.sub(r"[^a-zA-Z\s]", "", link.text).strip()

                msg += f"{title}\n{get_link(link['href'])}\n\n"
            await interaction.response.edit_message(content="```" + msg + "```")
        else:
            await interaction.channel.send(f"<@{interaction.user.id}> thats all...")

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, item):
        if self.pos + 1 <= len(self.links) // 10 and interaction.user.id == self.user_id:
            self.pos += 1

            msg = ""
            for res in self.links[self.pos * 10:(self.pos + 1) * 10]:
                link = res.find("a")
                title = re.sub(r"[^a-zA-Z\s]", "", link.text).strip()

                msg += f"{title}\n{get_link(link['href'])}\n\n"
            await interaction.response.edit_message(content="```" + msg + "```")
        else:
            await interaction.channel.send(f"<@{interaction.user.id}> thats all...")