from app.runner import twitter, mongo

# converts each item to a store in redis for intermediates, and stores the final
#  result in mongo (by a last job). Adds a callback field to each function that
#  calls a python function when the job finishes.
# @jobify
def request_user(username):
    # do some request magic: check and see if the user is stored
    #  else make api call
    user_data = {
        'username': 'buckbaskin'
    }
    result = mongo.enqueue(store_user, user_data)
    return 0

def store_user(user_data):
    # do some storage magic
    return 0

def user_start(username):
    result = twitter.enqueue(request_user, username)
    return 0
