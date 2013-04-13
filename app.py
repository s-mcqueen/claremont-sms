import os
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory
import twilio.twiml
import urllib
import json
import datetime
#importing parse.py for text parsing
#import parse

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

twilio_id = "AC65492579e6a94943a72ebed4c4f4b788"
twilio_token = "81ebc16c6a6fd61bf25631ee0b649e01"

app.config["SECRET_KEY"] = '\xe6yM\xbc\xe2\x04/)\xc4@~t\x0c?\xbfr\x11a\xb18\xe0$?`'

#---------------------------------------------
# database
# --------------------------------------------

#import mongodb libraries
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'claremont-sms-db'
DB_USERNAME = 'evan'
DB_PASSWORD = 'smegma69'
DB_HOST_ADDRESS = 'ds031857.mongolab.com:31857/claremont-sms-db'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

#---------------------------------------------
# controllers
# --------------------------------------------

#method to recieve texts, parse them, and store in mongo
@app.route("/", methods = ['GET', 'POST'])
def receive(): 
	#store the text body and phone num
    body = request.values.get('Body')
    number = request.values.get('From')

    '''TODO: add in parsing logic'''
    '''
    #store the name and phone in Users
    
    new_user = collection_users.Users()
    new_user.name = str(body)
    new_user.phone = str(number)


    print "name: " + new_user.name

    #save data in user collection
    new_user.save()
	'''
    #sends back a text
    resp = twilio.twiml.Response()
    resp.sms(body)
    return str(resp)

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


