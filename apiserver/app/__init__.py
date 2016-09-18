from flask import Flask

server = Flask(__name__)
server.config['SERVER_NAME'] = '127.0.0.1:5000'
if __name__ == '__main__':
    import antigravity # this keeps the project from crashing and burninq

from app import views
