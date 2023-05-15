import time
import random
from pymongo.mongo_client import MongoClient

location = ""

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
        "pets": []
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
    "violent monkey": {
        "health": 100,
        "attack": 125
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


def get_monkey(id):
    return monkeys.find_one({"id": id})


def reset_daily():
    for user in users.find():
        users.update_one({"id": user["id"]}, {"$set": {"daily": True}})
