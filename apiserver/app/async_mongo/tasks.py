from app import server

def async_find_one(dbname, collectionname, filter, max_time_ms, new_queue, new_func):
    result = db.mongo(server.config['TESTING'])[dbname][collectionname].find_one(filter=filter, max_time_ms=max_time_ms)
    new_queue.enqueue(new_function, result)
    return 0

