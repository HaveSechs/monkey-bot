import time
import random
from dotenv import dotenv_values
from pymongo.mongo_client import MongoClient

vals = dotenv_values(".env")
location = vals["MONGO"]

client = MongoClient(location)
database = client["Monkey"]
users = database["users"]
monkeys = database["monkeys"]

try:
    client.admin.command("ping")
    print("MonkeyDB is on")
except Exception as e:
    print(e)


def new_user(id: int, balance=0, daily=True):
    users.insert_one({
        "id": id,
        "balance": balance,
        "daily": daily,
        "inventory": {},
        "pets": [],
        "deck": [None, None, None, None, None]
    })


def get_user(id: int):
    return users.find_one({"id": id})


def set_money(id: int, amount: int):
    users.update_one({"id": id}, {"$set": {"balance": amount}})


def set_daily(id: int, val: bool):
    users.update_one({"id": id}, {"$set": {"daily": val}})


def set_inventory(id: int, inv: dict):
    users.update_one({"id": id}, {"$set": {"inventory": inv}})


def set_pets(id: int, pets: list):
    users.update_one({"id": id}, {"$set": {"pets": pets}})


stats = {
    "basic monkey": {
        "health": 100,
        "attack": 100
    },
    "wizard monkey": {
        "health": 100,
        "attack": 75
    },
    "violent monkey": {
        "health": 100,
        "attack": 125
    },
    "zombie monkey": {
        "health": 50,
        "attack": 100
    },
    "dj monkey": {
        "health": 100,
        "attack": 100
    },
    "soldier monkey": {
        "health": 125,
        "attack": 125
    },
    "gorilla": {
        "health": 1000,
        "attack": 800
    },
    "albino monkey": {
        "health": 200,
        "attack": 200
    },
    "kkk monkey": {
        "health": 100,
        "attack": 200
    }
}


def new_monkey(type):
    health = int((1 + (random.randint(-50, 50) / 100)) * stats[type]["health"])
    attack = int((1 + (random.randint(-50, 50) / 100)) * stats[type]["attack"])

    monkey_id = int(str(bin(int(time.time())))[2:] + format(random.randint(0, 255), "08b"), 2)

    monkeys.insert_one({
        "type": type,
        "health": health,
        "attack": attack,
        "id": monkey_id
    })

    return monkey_id


def get_monkey(id: int):
    return monkeys.find_one({"id": id})


def reset_daily():
    for user in users.find():
        users.update_one({"id": user["id"]}, {"$set": {"daily": True}})


def set_deck(id: int, slot: int, monkey: int):
    user = users.find_one({"id": id})
    user["deck"][slot] = monkey
    users.update_one({"id": id}, {"$set": {"deck": user["deck"]}})


def delete_pet(id: int):
    monkeys.delete_one({"id": id})


def change_pet_stats(id: int, json_data):
    monkeys.update_one({"id": id}, {"$set": json_data})


def remove_from_deck_and_pets(id: int, pet: id):
    user = get_user(id)
    user["pets"].remove(pet)
    if pet in user["deck"]:
        user["deck"].remove(pet)

    users.update_one({"id": id}, {"$set": {"deck": user["deck"]}})
    users.update_one({"id": id}, {"$set": {"pets": user["pets"]}})
