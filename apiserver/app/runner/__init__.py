from redis import StrictRedis
from rq import Queue

from app.util import cache

host = 'localhost'
port = 6379

class QueueMock(Queue):
    def __init__():
        pass

@cache
def funnel(mock=False):
    if mock:
        return QueueMock('funnel')
    else:
        return Queue('funnel', connection=StrictRedis(host=host, port=port, db=0))

@cache
def twitter(mock=False):
    if mock:
        return QueueMock('twitter')
    else:
        return Queue('twitter', connection=StrictRedis(host=host, port=port, db=0))

@cache
def mongo(mock=False):
    if mock:
        return QueueMock('mongo')
    else:
        return Queue('mongo', connection=StrictRedis(host=host, port=port, db=0))
