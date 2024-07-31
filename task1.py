import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


username = "fesho37"
password = "HaHaNorm095"
dbname = "cats_database"


uri = f"mongodb+srv://{username}:{password}@cluster0.yoxuueu.mongodb.net/{dbname}?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client[dbname]
collection = db['cats_collection']


def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    result = collection.insert_one(cat)
    print(f"Created cat with id: {result.inserted_id}")


def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)


def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat found with name: {name}")


def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Updated cat's age to {new_age}")
    else:
        print(f"No cat found with name: {name}")


def add_feature_to_cat(name, new_feature):
    result = collection.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
    if result.modified_count > 0:
        print(f"Added feature '{new_feature}' to cat with name: {name}")
    else:
        print(f"No cat found with name: {name}")


def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Deleted cat with name: {name}")
    else:
        print(f"No cat found with name: {name}")


def delete_all_cats():
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} cats")

if __name__ == "__main__":

    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_feature_to_cat("barsik", "любить гратись")
    delete_cat_by_name("barsik")
    delete_all_cats()