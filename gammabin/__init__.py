import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config


app = Flask(__name__)
conf = config.Config('config.json')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This flag tells the program it's deployed on heroku
if 'HEROKU' in os.environ:
    conf.add(('HEROKU', 1))

# Load app name from environment if it's not in the config
if ('APPNAME' in conf.config and
    conf.config['APPNAME']=="" and
    'APPNAME' in os.environ):
    conf.add(('APPNAME', os.environ['APPNAME']))

# Load admin key and secret key from environment
if 'ADMINSECRET' in os.environ:
    conf.add(('ADMINSECRET', os.environ['ADMINSECRET']))

if 'SECRETKEY' in os.environ:
    conf.add(('SECRETKEY', os.environ['SECRETKEY']))

# Set the secret key
if 'SECRETKEY' in conf.config:
    app.secret_key = conf.config['SECRETKEY']
else:
    exit("Secret key not set.")

db = SQLAlchemy(app)

from gammabin.models import *

db.create_all()

from . import api, views