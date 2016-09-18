from app import server
from app.twitter_api import views
from app.twitter_api import tasks as twitter_tasks

from app.db import mongo
from app.runner import funnel

from flask import render_template, make_response

# a default route to display information
@server.route('/', methods=('GET',))
def index():
    return render_template('index.html')

@server.route('/u/<username>', methods=('GET', 'POST',))
def user_read(username):
    '''
    users
     |- stored data (calculated info about this user)
     |- metadata (cached information from twitter about user)
     |- active (users that have logged in here)
    '''
    db = mongo()['users']
    collection = db['stored_data']
    result = funnel().enqueue(twitter_tasks.user_start, username)
    print('start request')
    request = {'username': username}
    result = collection.find_one(filter=request, max_time_ms=100)
    print('result = %s' % (result,))
    if result:
        return make_response(result, 200)
    else:
        return make_response('User Not Found', 404)

@server.route('/u/<username>/basics', methods=('GET', 'POST',))
def user_start(username):
    db = mongo()['users']
    collection = db['stored_data']
    result = funnel().enqueue(twitter_tasks.user_start, username)
    return make_response('OK', 200)

