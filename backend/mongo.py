from pymongo import MongoClient

from backend import settings


database = MongoClient(settings.MONGO_CONNECTION_STRING)
