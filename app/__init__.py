# this code allows us to import modules inside the lib directory
import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  

from flask import Flask
#from mongoengine import connect
#from flask.ext.mongoengine import MongoEngine
from lib import tokens
# import twilio.twiml
from twilio.rest import TwilioRestClient

DB_NAME = 'claremont-sms-db'
DB_USERNAME = 'evan'
DB_PASSWORD = 'smegma69'
DB_HOST_ADDRESS = 'ds031857.mongolab.com:31857/claremont-sms-db'

# init

app = Flask(__name__)
app.config.from_object('config')
app.debug = True

# db init

# app.config["MONGODB_DB"] = DB_NAME 
# connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)

# db = MongoEngine(app)

# twilio init

client = TwilioRestClient(tokens.TWILIO_ID, tokens.TWILIO_TOKEN)
