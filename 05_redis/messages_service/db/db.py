import pymongo
from pymongo.asynchronous import collection

from constants import mongo as mongo_constants

def get_collection() -> collection.AsyncCollection:
    client = pymongo.AsyncMongoClient(mongo_constants.MONGO_URL)
    db = client.get_database(mongo_constants.DB_NAME)    
    return db.get_collection(mongo_constants.COLLECTION_NAME)
