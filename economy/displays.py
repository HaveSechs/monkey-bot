import discord
import database
import visuals.monkie
from discord.ext import commands
from discord import app_commands
from utilities.utilities import autocomplete_id


class displayEconomy(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config
        # self.tree = app_commands.CommandTree(self.monkey)

    @app_commands.command(name="balance", description="check how broke you are")
    async def balance(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Balance", color=0x336EFF)
        embed.add_field(name="Money", value=f"{user['balance']} :monkey_face:", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="its not about what you have, its about what you don't have")
    async def inventory(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Inventory", color=0x336EFF)

        for item in user["inventory"]:
            embed.add_field(name=f"{item} - {user['inventory'][item]['amount']}", value=self.config["items"][item]["description"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pets", description="nesi is no longer my pet")
    async def pets(self, interaction: discord.Interaction, who: discord.User = None):
        if who is None:
            who = interaction.user

        user = database.get_user(who.id)
        if user is None:
            database.new_user(who.id)
            user = database.get_user(who.id)

        embed = discord.Embed(title=f"{who.name}'s Pets", color=0x336EFF)

        for pet in user["pets"][:10]:
            info = database.get_monkey(pet)
            try:
                embed.add_field(name=info["type"] + f" ({info['id']})", value=f":heart: {info['health']} :dagger: {info['attack']}", inline=False)
            except:
                print(pet)

        pets = [[]]
        cnt = 0
        for pet in range(len(user["pets"])):
            if pet % 10 == 0 and pet != 0:
                pets.append([])
                cnt += 1
            else:
                pets[cnt].append(user["pets"][pet])

        await interaction.response.send_message(embed=embed, view=visuals.monkie.petsDisplay(pets, interaction.user))

    @app_commands.command(name="shop", description="look at all the things you can't afford")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Shop", color=0x336EFF)

        for item in self.config["shop"].keys():
            shop = self.config["shop"]
            embed.add_field(name=f"{item} - {shop[item]['price']} :monkey_face:", value=self.config["items"][item]["description"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="multipliers", description="boosting ur dumbness")
    async def multipliers(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Multipliers", color=0x336EFF)
        embed.add_field(name="Message", value=f"{self.config['message_multiplier']}", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="chances", description="create your own luck...")
    async def chances(self, interaction: discord.Interaction):
        ch = ""
        for monkey in self.config["chances"]["monkeys"]:
            ch += f"`{monkey} - {self.config['chances']['monkeys'][monkey] * 100}`\n"
        ch += f"`{sum(list(self.config['chances']['monkeys'].values())) * 100}`"

        embed = discord.Embed(title="Chances", color=0x336EFF)
        embed.add_field(name="", value=ch)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quests", description="view your epik journey")
    async def quests(self, interaction: discord.Interaction):
        user = database.get_user(interaction.user.id)
        if user is None:
            database.new_user(interaction.user.id)
            user = database.get_user(interaction.user.id)

        embed = discord.Embed(title="Quests", color=0x00ff99)

        for quest in user["quests"]:
            reward = ""
            rewards = self.config['quests'][quest[0]]['rewards']
            if "money" in rewards:
                reward += f":monkey:{rewards['money']}"
            if "monkey" in rewards:
                reward += f"{self.config['monkey_emojis'][rewards['monkey']]}"
            if "item" in rewards:
                reward += f"{rewards['items']}"
            embed.add_field(name=self.config['quests'][quest[0]]['desc'], value=f"Rewards: {reward} {quest[1]}/{self.config['quests'][quest[0]]['total']}", inline=False)

        await interaction.response.send_message(embed=embed, view=visuals.monkie.claimQuests(interaction.user.id, self.config))


async def setup(monkey, config):
    await monkey.add_cog(displayEconomy(monkey, config))
