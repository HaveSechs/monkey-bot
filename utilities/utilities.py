import json
import discord
import database
from discord.ext import commands
from discord import app_commands

import pandas as pd
import joblib
import nltk
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


class utilities(commands.Cog):
    def __init__(self, monkey, config):
        self.monkey = monkey
        self.config = config

    @app_commands.command(name="suggest", description="random")
    async def suggest(self, interaction: discord.Interaction, sentence: str):
        if len(sentence.split()) < 3:
            await interaction.response.send_message("too short bozo")
        else:
            with open("suggestions.txt", "a") as f:
                f.write(sentence + "\n")

            await interaction.response.send_message("done")


async def setup(monkey, config):
    await monkey.add_cog(utilities(monkey, config))