from pymongo import MongoClient


def get_client():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    db = client["data_raw_befood"]
    return db["restaurants"]

print(get_client())