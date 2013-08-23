# this code allows us to import modules inside the lib directory
import sys, os 
sys.path.insert(0, os.path.abspath(".."))

from flask import Flask
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
from lib import tokens
import twilio.twiml
from twilio.rest import TwilioRestClient

# init

import config

app = Flask(__name__)
app.config.from_object('config')
app.debug = True

# db init

app.config["MONGODB_DB"] = 'claremont-sms-db' 
connect('claremont-sms-db', host='mongodb://' + 'evan' + ':' + tokens.DB_PASSWORD + '@' + tokens.DB_HOST_ADDRESS)

db = MongoEngine(app)

from views import *

# twilio init

client = TwilioRestClient(tokens.TWILIO_ID, tokens.TWILIO_TOKEN)
