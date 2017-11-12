from flask import Flask
from flask_cors import CORS
from flask_oauth import OAuth
from flask_sqlalchemy import SQLAlchemy

from .intuit import BASE_URL
from .intuit import CLIENT_ID, CLIENT_SECRET
from .intuit import REDIRECT_URI, AUTH_BASE_URL, ACCESS_BASE_URL, REQUEST_BASE_URL
from .intuit import SCOPE

# Create flask app and configure it
app = Flask(__name__)
app.config.from_object('app.config.DevConfig')

# Allow CORS
CORS(app)

# OAuth for interfacing with QBO
oauth = OAuth()
qbo = oauth.remote_app('QuickBooks',
    base_url=BASE_URL,
    request_token_url=None,
    access_token_url=ACCESS_BASE_URL,
    authorize_url=AUTH_BASE_URL,
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={
        'scope': SCOPE,
        'response_type': 'code',
        'state': 'MERDE',
    }
)

# Init SQLAlchemy engine
db = SQLAlchemy(app)

# Import routes so flask works
from app import views
