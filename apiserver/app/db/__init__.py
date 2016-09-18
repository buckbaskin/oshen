from pymongo import MongoClient
from bson import ObjectId

from app.util import cache

class MongoMock(MongoClient):
    pass

@cache
def mongo(mock=False):
    if mock:
        return MongoMock()
    else:
        return MongoClient('127.0.0.1', 27017)

def bson2json(bson):
    try:
        bson['_id'] = str(bson['_id'])
    except KeyError:
        return bson
    return bson

