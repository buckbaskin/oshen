from pymongo import MongoClient

from app.util import cache

class MongoMock(MongoClient):
    def __init__():
        pass

@cache
def mongo(mock=False):
    if mock:
        return MongoMock()
    else:
        return MongoClient('127.0.0.1', 27017)
