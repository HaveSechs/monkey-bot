import re
import json
import discord
import asyncio
import database
import aiohttp
from . import tor
from discord.ext import commands
from discord import app_commands
from bs4 import BeautifulSoup

import nltk
import joblib
import pandas as pd
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

classifier_lr_off_from_joblib = joblib.load('assets/ai/classifier_lr_off.pkl')
classifier_lr_hate_from_joblib = joblib.load('assets/ai/classifier_lr_hate.pkl')
df = pd.read_csv("assets/ai/hatespeech.csv")

with open("config.json") as f:
    config = json.load(f)


async def autocomplete_id(interaction: discord.Interaction, id: int):
    user = database.get_user(interaction.user.id)

    if user is None:
        database.new_user(interaction.user.id)
        user = database.get_user(interaction.user.id)

    choices = []

    for id in user["pets"]:
        monkey = database.get_monkey(id)

        name = f"{monkey['type']} 🐵 {monkey['health']} ❤️ {monkey['attack']} 🗡️"

        choices.append(
            app_commands.Choice(name=name, value=str(id))
        )

    return choices


def is_racist(message, queue):
    data = message.content.lower()
    df['tweet'][0] = data
    corpus = []
    for i in range(0, 24783):
        review = df['tweet'][i]
        review = review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
        review = ' '.join(review)
        corpus.append(review)
    cv = CountVectorizer(max_features=2000)
    X = cv.fit_transform(corpus).toarray()
    pred = classifier_lr_off_from_joblib.predict(X[:1])[0] + classifier_lr_hate_from_joblib.predict(X[:1])[0]

    if pred > 0:
        queue.append({"id": message.id, "cid": message.channel.id, "result": pred})


def get_link(url):
    url = url.split("http://")
    return "http://" + url[-1]


class utilities(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config
        self.queue = []

        asyncio.ensure_future(self.send_screenshots())

    async def send_screenshots(self):
        while True:
            if len(self.queue) > 0:
                ss = self.queue[0]

                channel = await self.monkey.fetch_channel(ss["cid"])
                await channel.send(f"<@{ss['id']}>", file=ss["file"])

                self.queue.pop(0)
            await asyncio.sleep(1)

    @app_commands.command(name="suggest", description="random")
    async def suggest(self, interaction: discord.Interaction, sentence: str):
        if len(sentence.split()) < 3:
            await interaction.response.send_message("too short bozo")
        else:
            with open("suggestions.txt", "a") as f:
                f.write(sentence + "\n")

            await interaction.response.send_message("done")

    @app_commands.command(name="tor", description="i chose a browser without cp hahaha lmao")
    async def tor(self, interaction: discord.Interaction, query: str):
        print("started", query)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ahmia.fi/search/?q={query}") as req:
                html = await req.text()

        msg = ""

        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all(class_="result")

        for res in results[:10]:
            link = res.find("a")
            title = re.sub(r"[^a-zA-Z\s]", "", link.text).strip()

            msg += f"{title}\n{get_link(link['href'])}\n\n"
        print(msg)

        try:
            await interaction.response.send_message("```" + msg + "```")
        except:
            await interaction.channel.send(f"<@{interaction.user.id}> it took longer than 3 seconds so...\n```" + msg + "```")

    @app_commands.command(name="screenshot", description="nesi told me not to do this")
    async def screenshot(self, interaction: discord.Interaction, url: str):
        # loop = asyncio.get_event_loop()
        file = await tor.capture_screenshot(url)
        self.queue.append(
            {"cid": interaction.channel.id, "id": interaction.user.id, "file": file}
        )


async def setup(monkey, config):
    await monkey.add_cog(utilities(monkey, config))