from app import server

from nose.tools import ok_, assert_equal

def setup_module():
    global test_client
    test_client = server.test_client()

def test_index():
    response = test_client.get('/')
    assert_equal(response.status_code, 200)

def test_user_read():
    response = test_client.get('/u/bebaskin')
    assert_equal(response.status_code, 200)

def test_user_start():
    response = test_client.get('/u/bebaskin/start')
    assert_equal(response.status_code, 200)

