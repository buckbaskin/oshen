import app
from app import runner, db
from app import server
from app.twitter_api import API

import urllib
from twitter import TwitterHTTPError
import time

def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except urllib.error.URLError as e:
            print('Network error')
            raise e
        except TwitterHTTPError as e:
            print('Rate limited')
            for i in range(15, 1, -1):
                print('%s minutes remaining.' % (i,))
                time.sleep(60)
            raise e
    return wrapper

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
    api_data = handle_api_error(API().users.lookup)(
        screen_name=str(username).lower(), include_entities=True
    )
    for user in api_data:
        if 'screen_name' in user:
            user['screen_name'] = str(user['screen_name']).lower()
            result = runner.mongo(server.config['TESTING']).enqueue(store_user, user)
            result = runner.mongo().enqueue(request_followers, str(username).lower())
    return 0

def request_1K_tweets(username):
    print('r1Kt: for username %s' % (username,))
    last_max_id = -2
    count = 0
    max_id = -1
    api_data = []
    while max_id != last_max_id and count < 10:
        last_max_id = max_id
        if max_id != -1:
            print('next api data!')
            api_data = handle_api_error(API().statuses.user_timeline)(
                screen_name=username, count=10, trim_user='true',
                exclude_replies='false', contributor_details='false',
                include_rts='true', max_id=max_id
            )
        else:
            api_data = handle_api_error(API().statuses.user_timeline)(
                screen_name=username, count=10, trim_user='true',
                exclude_replies='false', contributor_details='false',
                include_rts='true'
            )
        print('r1Kt: found %s tweets' % (len(api_data),))
        for tweet in api_data:
            runner.mongo().enqueue(store_tweet, args=(username, tweet,))
            if tweet['id'] < max_id or max_id == -1:
                max_id = tweet['id']
        count += 10

def request_followers(username):
    current_cursor = -1
    last_cursor = -2
    list_of_follower_screen_names = []
    while current_cursor != last_cursor:
        last_cursor = current_cursor + 0
        api_data = handle_api_error(API().followers.list)(
            screen_name=username, cursor=current_cursor, count=200
        )
        for user in api_data['users']:
            list_of_follower_screen_names.append(
                str(user['screen_name']).lower()
            )
            runner.mongo().enqueue(store_user, user)
            runner.twitter().enqueue(
                request_1K_tweets, user['screen_name'], timeout=10000
            )
        current_cursor = api_data['next_cursor']
    database = db.mongo(server.config['TESTING'])['users']
    collection = database['metadata']
    collection.find_one_and_update(
        {'screen_name': str(username).lower()},
        {'$addToSet': {'follower_screen_names': list_of_follower_screen_names}}
    )

def store_user(user_data):
    # do some storage magic
    user_data['screen_name'] = str(user_data['screen_name']).lower()
    database = db.mongo()['users']
    collection = database['metadata']
    collection.insert_one(user_data)
    return 0

def store_tweet(username, tweet_data):
    try:
        tweet_data['user']['screen_name'] = (
            str(tweet_data['user']['screen_name']).lower()
        )
    except KeyError:
        pass
    database = db.mongo()['users']
    collection = database['tweets']
    print('store_tweet: mongo[users][tweets]')
    collection.find_one_and_update(
        {'screen_name': str(username).lower()},
        {'$addToSet': {'tweets' : [tweet_data]}}, upsert=True
    )
    return 0

def user_start(username):
    runner.twitter(server.config['TESTING']).enqueue(request_user, username, timeout=10000)
    return 0

def filter_retweets(username):
    '''
    Set aside all retweets by the given username
    '''
    # TODO(buckbaskin):
    # get all stored tweets from a user
    # loop over them and remove the non-retweets
    # store the retweets in their own location
    database = db.mongo()['users']
    collection = database['tweets']
    data = collection.find_one({'screen_name': str(username).lower()})
    # print('data! %s' % (data,))
    collection = database['retweets']
    if not collection.find_one():
        try:
            user_tweets = data['tweets'][0]
            for tweet in user_tweets:
                print('%s said %s' % (username, tweet['text']))
                for word in tweet['text'].split(' '):
                    print('word: %s' % (word,))
                    collection.find_one_and_update({}, {'$inc' : {word.lower() : 1}}, upsert=True)
        except TypeError as e:
            pass
    return 0

def filter_follower_retweets(username, next_queue, next_function):
    '''
    For all followers of a user, set aside retweets
    '''
    # TODO(buckbaskin):
    # aggregate the list of followers
    # loop over them and queue up the filter_retweets
    print('start of function')
    database = db.mongo()['users']
    collection = database['metadata']
    followers = collection.find_one({'screen_name': str(username).lower()})['follower_screen_names'][0]
    print('followers: %s' % (followers,))
    for follower in followers:
        runner.analysis().enqueue(filter_retweets, args=(follower, ))
    getattr(runner, next_queue)().enqueue(getattr(app.twitter_api.tasks, next_function), username)
    return 0

def analyze_retweets(username, primary_user):
    '''
    For an individual follower, aggregate information about the retweets, and
    append to the information for the primary user.
    '''
    # TODO(buckbaskin):
    return 0

def analyze_follower_retweets(username):
    '''
    Process follower retweets
    '''
    # TODO(buckbaskin):
    # run against all followers
    database = db.mongo()['users']
    collection = database['retweets']
    result = collection.find_one()
    new_list = []
    for item in result.items():
        try:
            new_list.append((item[0], int(str(str(item[1])+'')),))
        except TypeError:
            pass
        except ValueError:
            pass
    print(sorted(new_list, key=lambda x: -x[1])[:50])
    return 0

def user_run_analysis(username):
    database = db.mongo(server.config['TESTING'])['users']
    collection = database['metadata']
    request = {'screen_name': str(username).lower()}
    result = collection.find_one(filter=request, max_time_ms=1000)
    if not result:
        # if the result is not there, do a user start
        runner.funnel().enqueue(user_start, username)
    # filter follower retweets, then run analysis on them
    runner.analysis().enqueue(
        filter_follower_retweets,
        args=(username, 'analysis', 'analyze_follower_retweets',)
    )

def user_start_analysis(username):
    runner.analysis().enqueue(user_run_analysis, username)
