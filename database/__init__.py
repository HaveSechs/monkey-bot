from pymongo.mongo_client import MongoClient

location = ""

client = MongoClient(location)
database = client["Monkey"]
users = database["users"]

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
        "inventory": {}
    })


def get_user(id: int):
    return users.find_one({"id": id})


def set_money(id: int, amount: int):
    users.update_one({"id": id}, {"$set": {"balance": amount}})
