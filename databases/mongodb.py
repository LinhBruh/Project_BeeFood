from pymongo import MongoClient

uri = "mongodb://admin:password@localhost:27017/"
client = MongoClient(uri)
db = client["data_raw_befood"]
collection = db["mon_a_au"]

print(collection.find_one())