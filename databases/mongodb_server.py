import pymongo
import pprint

client = pymongo.MongoClient("mongodb://localhost:60000/")

# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
# mydict = { "name": "John", "address": "Highway 37" }
# x = mycol.insert_one(mydict)

db = client["database"]
collection = db["authors"]

posts = db.posts
post = {"author": "Ananmay", "text": "My First Database!"}

result = collection.insert_one(post)

print(result.inserted_id)
