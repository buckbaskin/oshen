from app import server, db

def async_find_one(dbname, collectionname, filter_, max_time_ms, new_queue, new_function):
    result = db.mongo(server.config['TESTING'])[dbname][collectionname].find_one(filter=filter_, max_time_ms=max_time_ms)
    new_queue.enqueue(new_function, result)
    return 0

