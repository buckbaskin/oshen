from redis import StrictRedis
from rq import Queue

class QueueMock(Queue):
    def __init__():
        pass

def funnel(mock=False):
    if mock:
        return QueueMock()
    else:
        if funnel.__cached__ is None:
            funnel.__cached__ = Queue(connection=StrictRedis(host='127.0.0.1', port=6379, db=0))
        return funnel.__cached__
funnel.__cached__ = None
