from app import server
from app.twitter_api import views
from app.twitter_api import tasks as twitter_tasks

from app.db import mongo, bson2json
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
    db = mongo(server.config['TESTING'])['users']
    collection = db['metadata']
    result = funnel(server.config['TESTING']).enqueue(twitter_tasks.user_start, username)
    request = {'screen_name': str(username).lower()}
    print('start request %s' % (request,))
    result = collection.find_one(filter=request, max_time_ms=100)
    print('result = %s' % (result,))
    if result:
        print('result niceness')
        return make_response(str(bson2json(result)), 200)
    else:
        print('unf result')
        return make_response('User Not Found', 404)

@server.route('/u/<username>/start', methods=('GET', 'POST',))
def user_start(username):
    db = mongo(server.config['TESTING'])['users']
    collection = db['stored_data']
    result = funnel(server.config['TESTING']).enqueue(twitter_tasks.user_start, username)
    return make_response('OK', 200)

