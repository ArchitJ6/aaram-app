import secrets
from config import *
from flask import Flask, render_template

from app.authentication.auth import authentication
from app.redirect.main import redirect_
from app.user_data.main import profile
from app.hallway.main import socketio
from app.feed.main import feed

DB_PATH = './database/login_info.sqlite'

app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(32)
socketio.init_app(app, cors_allowed_origins='*')

app.register_blueprint(authentication, url_prefix='/authentication')
app.register_blueprint(redirect_, url_prefix='')
app.register_blueprint(profile, url_prefix='/profile_data')
app.register_blueprint(feed, url_prefix='/feed')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, host=IP, port=PORT)