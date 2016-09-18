from app import runner, db
from app import server

# converts each item to a store in redis for intermediates, and stores the final
#  result in mongo (by a last job). Adds a callback field to each function that
#  calls a python function when the job finishes.
# @jobify
def request_user(username):
    # do some request magic: check and see if the user is stored
    database = db.mongo(server.config['TESTING'])['users']
    collection = database['metadata']
    request = {'username': username}
    result = collection.find_one(filter=request, max_time_ms=1000)
    if result:
        # break chain, the user data is already there
        return 0

    #  else make api call
    user_data = {
        'username': 'bebaskin',
        'description': 'n days since last major coding hazard',
        'age': 'old as dirt'
    }
    # print('request_user: username %s got type %s of size %s' % (username, type(user_data), len(user_data),))
    result = runner.mongo(server.config['TESTING']).enqueue(store_user, user_data)
    return 0

def store_user(user_data):
    # do some storage magic
    print('store_user: storing user_data %s' % (user_data,))
    db = db.mongo['users']
    collection = db['metadata']
    result = collection.insert_one(user_data)
    print('insert id %d' % (result.inserted_id,))
    return 0

def user_start(username):
    result = runner.twitter(server.config['TESTING']).enqueue(request_user, username)
    return 0
