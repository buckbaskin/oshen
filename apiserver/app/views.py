from app import server
from app.twitter_api import views

from flask import render_template

# a default route to display information
@server.route('/')
def index():
    return render_template('index.html')
