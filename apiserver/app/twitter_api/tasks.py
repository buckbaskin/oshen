from app import runner, db
from app import server
from app.twitter_api import API

# converts each item to a store in redis for intermediates, and stores the final
#  result in mongo (by a last job). Adds a callback field to each function that
#  calls a python function when the job finishes.
# @jobify
def request_user(username):
    # do some request magic: check and see if the user is stored
    database = db.mongo(server.config['TESTING'])['users']
    collection = database['metadata']
    request = {'screen_name': str(username).lower()}
    result = collection.find_one(filter=request, max_time_ms=1000)
    if False and result:
        # break chain, the user data is already there
        return 0

    #  else make api call
    api_data = API().users.lookup(screen_name=str(username).lower(), include_entities=True)
    for user in api_data:
        if 'screen_name' in user:
            user['screen_name'] = str(user['screen_name']).lower()
            result = runner.mongo(server.config['TESTING']).enqueue(store_user, user)
    return 0

def store_user(user_data):
    # do some storage magic
    print('store_user: storing user_data %s' % (user_data,))
    database = db.mongo()['users']
    collection = database['metadata']
    result = collection.insert_one(user_data)
    print('insert id %s' % (result.inserted_id,))
    return 0

def user_start(username):
    result = runner.twitter(server.config['TESTING']).enqueue(request_user, username)
    return 0
