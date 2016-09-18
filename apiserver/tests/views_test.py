from app import server
from app import db

from nose.tools import ok_, assert_equal

def setup_module():
    global test_client
    server.config['TESTING'] = True
    test_client = server.test_client()
    db.mongo(server.config['TESTING'])['users']['metadata'].insert_one({'username': bebaskin, 'age': 'old'})

def test_index():
    response = test_client.get('/')
    assert_equal(response.status_code, 200)

def test_user_read():
    response = test_client.get('/u/bebaskin')
    assert_equal(response.status_code, 200)

def test_user_start():
    response = test_client.get('/u/bebaskin/start')
    assert_equal(response.status_code, 200)

