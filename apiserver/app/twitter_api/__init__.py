import os
import twitter as it
from twitter.api import TwitterHTTPError

from app.util import cache

class TwitterMock(it.Twitter):
    pass

@cache
def API(mock=False):
    if mock:
        return TwitterMock()
    print('CWD: %s' % os.getcwd())
    with open('instance/twitterc.txt', 'r') as f:
        consumerKey = f.readline()[:-1]
        consumerSecret = f.readline()[:-1]
    if os.path.isfile('instance/twittera.txt'):
        with open('instance/twittera.txt') as f:
            accessToken = f.readline()[:-1]
            accessTokenSecret = f.readline()[:-1]
    else:
        accessToken, accessTokenSecret = it.oauth_dance('The Insight Project', consumerKey, consumerSecret, token_filename='instance/twittera.txt')
    
    return it.Twitter(auth=it.OAuth(accessToken, accessTokenSecret, consumerKey, consumerSecret)) 
