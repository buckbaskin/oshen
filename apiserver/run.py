

from app import server

def setup_mongo():
    pass

def setup_redis():
    pass

if __name__ == '__main__':
    setup_mongo()
    setup_redis()
    server.run()
