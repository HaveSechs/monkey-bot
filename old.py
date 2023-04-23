# https://www.google.com/search?q={}&source=lnms&tbm=isch

import time
import json
import random
import buttons
import discord
import requests
import threading
from bs4 import BeautifulSoup
from discord import app_commands
from google_trans_new import google_translator

translator = google_translator()
monkey = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(monkey)

whitelist = {1078446734700716164, 1082482837783060620}
dont = {1077343088642637824, 1077345122355777679, 1077345168203710685}
admin = {997660032592261120, 894709733343264829, 1092243583735705601}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


def daily_checker():
    if int(time.time()) % 86400 == 0 or 1:
        with open("db.json", "r") as f:
            db = json.load(f)

        for user in db.keys():
            db[user]["daily"] = True

        with open("db.json", "w") as f:
            json.dump(db, f)


@monkey.event
async def on_ready():
    threading.Thread(target=daily_checker).start()
    await monkey.change_presence(activity=discord.Game("With Children"))
    await monkey.wait_until_ready()
    await tree.sync()
    print("ready")


@monkey.event
async def on_member_join(member):
    print(member.id)
    if int(member.id) == 1082279448155537498:
        await member.ban(reason="nuke")
    content = f"<@{member.id}> **5 invites = Free Admin**\n\nAnyways enjoy the true african experience"
    await member.send(content)


@monkey.event
async def on_message_delete(message):
    if int(message.channel.id) not in whitelist and int(message.author.id) != 1068008865901318184:
        await message.channel.send(f"\"{message.content}\"\n\n-<@{message.author.id}>")


@monkey.event
async def on_channel_delete(channel):
    if channel.id in dont:
        pass


def new_user(id, coins=0, daily=True):
    with open("db.json", "r") as f:
        bank = json.load(f)

    bank[id] = {"coins": coins, "inventory": {}, "daily": daily}

    with open("db.json", "w") as f:
        json.dump(bank, f)


def get_item(query, arr):
    results = []
    for item in arr:
        if query in item["title"].lower():
            results.append(item)
    return results


@monkey.event
async def on_message(message):
    coins = random.randint(0, 8)

    with open("db.json", "r") as f:
        bank = json.load(f)

    author = str(message.author.id)

    if author in bank:
        bank[author]["coins"] += coins

        with open("db.json", "w") as f:
            json.dump(bank, f)
    else:
        new_user(author, coins)


@tree.command(name="serverend", description="Checks when the server ends...")
async def send(interaction: discord.Interaction):
    await interaction.response.send_message(
        "<t:1683118800:R> this server will be ended by <@1069769427182162001>... :cry:")


@tree.command(name="translate", description="For my brazilian friends")
async def trans(interaction: discord.Interaction, what: str, src: str = "pt", dest: str = "en"):
    print(what, src, dest)
    text = translator.translate(what, lang_src=src, lang_tgt=dest)
    await interaction.response.send_message(text)


@tree.command(name="purge", description="don't chat in announcements...")
async def pur(interaction: discord.Interaction, cnt: int):
    if interaction.user.id in admin:
        await interaction.channel.purge(limit=cnt, check=lambda msg: not msg.pinned)
        await interaction.response.send_message(f"Purged {cnt} messages")


@tree.command(name="spam", description="roberto")
async def spam(interaction: discord.Interaction, text: str, cnt: int):
    if interaction.user.id in admin:
        for num in range(cnt):
            await interaction.response.send_message(f"Purged {cnt} messages")


@tree.command(name="img", description="notsobot but better")
async def google(interaction: discord.Interaction, query: str):
    bad_code = requests.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch", headers=headers).text
    res = []

    soup = BeautifulSoup(bad_code, 'html.parser')
    for item in soup.find_all('img'):
        try:
            if item['data-src'].split("/")[3].startswith("images"):
                res.append(item['data-src'])
        except:
            pass

    view = buttons.GoogleButton(res)

    await interaction.response.send_message(res[0], view=view)


@tree.command(name="scrape", description="for the langauge model")
async def scra(interaction: discord.Interaction):
    messages = interaction.channel.history(limit=None)

    with open("scraped.txt", "w") as f:
        f.write("[\n")
        async for message in messages:
            if len(message.clean_content.split()) >= 2:
                f.write('"' + message.clean_content.replace("\n", "").replace("```", "") + '",\n')
        f.write("]")


@tree.command(name="balance", description="your are so broke bruh")
async def bal(interaction: discord.Interaction, user: discord.User = None):
    with open("db.json", "r") as f:
        bank = json.load(f)

    if user is None:
        author = str(interaction.user.id)
    else:
        author = str(user.id)

    if author not in bank:
        new_user(author)

    with open("db.json", "r") as f:
        bank = json.load(f)

    embed = discord.Embed(title="Balance", color=0x336EFF)
    embed.add_field(name="Money", value=str(bank[author]["coins"]), inline=False)

    await interaction.response.send_message(embed=embed)


@tree.command(name="shop", description="spend your hard earned money")
async def shop(interaction: discord.Interaction):
    with open("shop.json", "r") as f:
        shop = json.load(f)

    embed = discord.Embed(title="Shop", color=0x336EFF)

    for item in shop:
        embed.add_field(name=f"{item['title']} - ${item['price']}", value=item['description'], inline=False)

    await interaction.response.send_message(embed=embed)


@tree.command(name="buy", description="buy stuff")
async def buy(interaction: discord.Interaction, item: str):
    with open("shop.json", "r") as f:
        shop = json.load(f)

    res = get_item(item, shop)

    if len(res) == 0:
        await interaction.response.send_message("it's non existent like ur dad")
    elif len(res) != 1:
        await interaction.response.send_message("not specific enough")
    else:
        with open("db.json", "r") as f:
            bank = json.load(f)

        author = str(interaction.user.id)

        if res[0]["price"] > bank[author]["coins"]:
            await interaction.response.send_message("omg you are so broke go get job")
        else:
            bank[author]["coins"] -= res[0]["price"]
            if res[0]["title"] not in bank[author]["inventory"]:
                bank[author]["inventory"][res[0]["title"]] = 1
            else:
                bank[author]["inventory"][res[0]["title"]] += 1

            with open("db.json", "w") as f:
                json.dump(bank, f)

            await interaction.response.send_message("enjoy")


@tree.command(name="inventory", description="flex your goods")
async def inventory(interaction: discord.Interaction, user: discord.User = None):
    with open("db.json", "r") as f:
        bank = json.load(f)

    if user is None:
        author = str(interaction.user.id)
    else:
        author = str(user.id)

    if author not in bank:
        new_user(author)

    with open("db.json", "r") as f:
        bank = json.load(f)

    embed = discord.Embed(title="Inventory", color=0x336EFF)

    for item in bank[author]["inventory"].keys():
        embed.add_field(name=f"{item} - {bank[author]['inventory'][item]}", value=" ", inline=False)

    await interaction.response.send_message(embed=embed)


@tree.command(name="daily", description="Daily bread and soup")
async def daily(interaction: discord.Interaction):
    with open("db.json", "r") as f:
        bank = json.load(f)

    author = str(interaction.user.id)

    if author in bank:
        if bank[author]["daily"] is True:
            bank[author]["coins"] += 100
            bank[author]["daily"] = False

            with open("db.json", "w") as f:
                json.dump(bank, f)
            await interaction.response.send_message("Added tokens!")
        else:
            await interaction.response.send_message("Daily is 24 hours not 2 seconds!")
    else:
        new_user(author, 100, False)
        await interaction.response.send_message("Added tokens!")


@tree.command(name="give", description="pay for free pics")
async def give(interaction: discord.Interaction, amount: int, recipient: discord.User):
    with open("db.json", "r") as f:
        bank = json.load(f)

    author = str(interaction.user.id)

    if author in bank:
        if bank[author]["coins"] >= amount:
            if str(recipient.id) not in bank:
                new_user(str(recipient.id), amount)
            else:
                bank[str(recipient.id)]["coins"] += amount
            bank[author]["coins"] -= amount

            with open("db.json", "w") as f:
                json.dump(bank, f)
            await interaction.resonse.send_message("ok richie")
        else:
            await interaction.resonse.send_message("ok brokie")
    else:
        new_user(author)
        await interaction.resonse.send_message("ok brokie")


monkey.run("MTA2ODAwODg2NTkwMTMxODE4NA.GKCPG4.9X5EbS8NES73JK0tbWyzP-MWR7dOc38hwD4lBo")
