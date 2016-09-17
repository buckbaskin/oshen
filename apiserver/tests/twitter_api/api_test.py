from app.twitter_api import API, APIMock

from nose.tools import ok_

def test_MockEqual():
    ok_(len(dir(API)), len(dir(APIMock)))
    ok_(dir(API) == dir(APIMock))

