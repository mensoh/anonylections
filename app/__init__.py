import os, config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, elections

