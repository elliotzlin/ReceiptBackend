from flask import Flask
from flask-sqlalchemy import SQLAlchemy

# Create flask app and configure it
app = Flask(__name__)
app.config.from_object('app.config.DevConfig')

# Init SQLAlchemy engine
db = SQLAlchemy(app)

# Import routes so flask works
from app import views
