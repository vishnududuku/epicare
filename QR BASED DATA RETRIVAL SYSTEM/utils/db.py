from pymongo import MongoClient

def get_db():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    db = client["medid"]  # Your database name
    return db
