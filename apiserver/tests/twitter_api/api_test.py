from app.twitter_api import API

from nose.tools import ok_

def skiptest_MockEqual():
    ok_(len(dir(API(True))), len(dir(API(False))))
    ok_(dir(API(True)) == dir(API(False)))

