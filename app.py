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
# models
# --------------------------------------------

#class to hold the message fields
class Message(Document):

	from_name = db.StringField(max_length=255)
	from_phone = db.StringField(max_length=15)
	message = db.StringField(max_length=400)
	to_name = db.StringField(max_length=255)
	created_at = db.DateTimeField(default=datetime.datetime.now)
	guess_id = db.StringField(max_length=5)

#class to hold the user fields
class User(db.DynamicDocument):

	name = db.StringField(max_length=255, unique=True)
	phone = db.StringField(max_length=15, unique=True)
	created_at = db.DateTimeField(default=datetime.datetime.now)

#---------------------------------------------
# controllers
# --------------------------------------------

"""
@app.route("/", methods = ['GET', 'POST']) 
def getMessages():
	#get all messages from the db
	messages = Messages.objects
	return messages
"""
@app.route("/", methods = ['GET', 'POST'])
def hello():
    return render_template('index.html')


#method to recieve texts, parse them, and store in mongo
@app.route("/receive", methods = ['GET', 'POST'])
def receive(): 
	#store the text body and phone num
    body = request.values.get('Body')
    number = request.values.get('From')

    # doesUserExist?
    # 	valid message?
    # 		get to number
    # 			is tonumber in db??
    # 				get message
    # 				forward
    # 	valid guess?
    # 		get guess number
    # 			is guess number in db?
    # 				get guess name
    # 				does it match?
    # 				send something
    # 	valid signup?
    # 		tell tehm you are already here!
    # 	valid stop?
    # 		remove them
    # else:
    # 	valid signup?
    # 		get signupname
    # 		sign them up
    # 	anything else:
    # 		fuck you, sign up!



    #tell new_user to look in the User collection
    new_user = User()
    
    #store the name and phone in Users
    new_user.name = str(body)
    new_user.phone = str(number)

    #save data in user collection
    new_user.save()

    print "exists: " + str(doesUserExist(number))

	
    #sends back a text
    resp = twilio.twiml.Response()
    resp.sms(body)
    return str(resp)

 def doesUserExist(phone_number):
 	if User.objects(phone = phone_number) is None:
 		return False
 	else:
 		return True

 



#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

