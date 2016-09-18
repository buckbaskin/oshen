from app import server
from app import db

from nose.tools import ok_, assert_equal

import pprint

def setup_module():
    global test_client
    server.config['TESTING'] = False
    test_client = server.test_client()

    database = db.mongo()['users']
    collection = database['metadata']
    request = {'screen_name': 'bebaskin', 'age': 'old'}
    pprint.pprint(request)
    collection.insert_one(request)

def test_index():
    response = test_client.get('/')
    assert_equal(response.status_code, 200)

def test_user_read():
    response = test_client.get('/u/bebaskin')
    assert_equal(response.status_code, 200)

def test_user_read_fail():
    response = test_client.get('/u/a')
    assert_equal(response.status_code, 404)

def test_user_start():
    response = test_client.get('/u/bebaskin/start')
    assert_equal(response.status_code, 200)

def test_user_analyze():
    response = test_client.get('/u/bebaskin/analyze')
    assert_equal(response.status_code, 200)
