from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Create flask app and configure it
app = Flask(__name__)
app.config.from_object('app.config.DevConfig')

# Allow CORS
CORS(app)

# Init SQLAlchemy engine
db = SQLAlchemy(app)

# Import routes so flask works
from app import views
