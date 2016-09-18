from redis import StrictRedis
from rq import Queue

from app.util import cache

class QueueMock(Queue):
    def __init__():
        pass

@cache
def funnel(mock=False):
    if mock:
        return QueueMock()
    else:
        return Queue(connection=StrictRedis(host='127.0.0.1', port=6379, db=0))
