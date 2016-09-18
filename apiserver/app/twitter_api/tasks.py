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
    list_of_follower_screen_names = []
    for user in api_data:
        if 'screen_name' in user:
            user['screen_name'] = str(user['screen_name']).lower()
            list_of_follower_screen_names.append(user['screen_name'])
            result = runner.mongo(server.config['TESTING']).enqueue(store_user, user)
            result = runner.mongo().enqueue(request_1K_tweets, str(username).lower())
            result = runner.mongo().enqueue(request_followers, str(username).lower())
    collection.find_one_and_update({'screen_name': str(username).lower()}, {'$push': {'follower_screen_names': list_of_follower_screen_names}})
    return 0

def request_1K_tweets(username):
    last_max_id = -2
    count = 0
    max_id = -1
    while(max_id != last_max_id and count < 1000):
        last_max_id = max_id
        if max_id != -1:
            api_data = API().statuses.user_timeline(screen_name=username, count=200, trim_user='true', exclude_replies='false', contributor_details='false', include_rts='true', max_id=max_id)

        for tweet in api_data:
            runner.mongo().enqueue(store_tweet, tweet)
            if tweet['id'] < max_id or max_id == -1:
                max_id = tweet['id']
        count += 200

def request_followers(username):
    current_cursor = -1
    last_cursor = -2
    while(current_cursor != last_cursor):
        last_cursor = current_cursor + 0
        api_data = API().followers.list(screen_name=username, cursor=current_cursor, count=200)
        for user in api_data['users']:
            runner.mongo().enqueue(store_user, user)
            runner.mongo().enqueue(request_1K_tweets, username)
        current_cursor = api_data['next_cursor']

def store_user(user_data):
    # do some storage magic
    user_data['screen_name'] = str(user_data['screen_name']).lower()
    database = db.mongo()['users']
    collection = database['metadata']
    result = collection.insert_one(user_data)
    return 0

def store_tweet(tweet_data):
    tweet_data['user']['screen_name'] = str(tweet_data['user']['screen_name']).lower()
    database = db.mongo()['users']
    collection = database['tweets']
    result = collection.insert_one(tweet_data)
    return 0

def user_start(username):
    runner.twitter(server.config['TESTING']).enqueue(request_user, username)
    return 0

def filter_retweets(username):
    '''
    Set aside all retweets by the given username
    '''
    # get all stored tweets from a user
    # loop over them and remove the non-retweets
    # store the retweets in their own location
    return 0

def filter_follower_retweets(username, next_queue, next_function):
    '''
    For all followers of a user, set aside retweets
    '''
    # aggregate the list of followers
    # loop over them and queue up the filter_retweets
    
    next_queue.enqueue(next_function, username)
    return 0

def analyze_retweets(username, primary_user):
    '''
    For an individual follower, aggregate information about the retweets, and 
    append to the information for the primary user.
    '''
    return 0

def analyze_follower_retweets(username, next_queue, next_function):
    '''
    Process follower retweets
    '''
    # run against all followers

    next_queue.enqueue(next_function, username)
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
    runner.analysis().enqueue(filter_follower_retweets, username, runner.analysis(), analyze_follower_retweets,)

def user_start_analysis(username):
    runner.analysis().enqueue(user_run_analysis, username)
