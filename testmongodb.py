import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI")


try:
    client = MongoClient(mongo_uri)
    client.admin.command('ping')
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("Error connecting to MongoDB Atlas:", e)
