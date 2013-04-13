import os
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory
import twilio.twiml
from twilio.rest import TwilioRestClient
import urllib
import json
import datetime
#importing parse.py for text parsing
import parse
import random

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

twilio_id = "AC65492579e6a94943a72ebed4c4f4b788"
twilio_token = "81ebc16c6a6fd61bf25631ee0b649e01"

client = TwilioRestClient(twilio_id, twilio_token)


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
class Message(db.DynamicDocument):

    from_name = db.StringField(max_length=255)
    from_phone = db.StringField(max_length=15)
    message = db.StringField(max_length=400)
    to_name = db.StringField(max_length=255)
    to_phone = db.StringField(max_length=15)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    guess_id = db.StringField(max_length=5) 

#class to hold the user fields
class User(db.DynamicDocument):

    name = db.StringField(max_length=255, unique=True)
    phone = db.StringField(max_length=15, unique=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    # guess_counter = db.StringField(max_length=5)
    
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
@app.route("/", methods = ['GET'])
def display():
    message = Message.objects(from_name='seanmcqueen').get()
    recipient = Message.objects(from_name='seanmcqueen').get()
    return render_template('index.html', message=message, name=recipient)


#method to recieve texts, parse them, and store in mongo
@app.route("/receive", methods = ['GET', 'POST'])
def receive(): 
	#store the text body and phone num
    body = request.values.get('Body')
    number = request.values.get('From')

    if numberExists(number):
        processExisting(body, number)

    # else:
    #     processNew(body, number)



#check if number exists already in users DB
def numberExists(phone_number):
 	if User.objects(phone = phone_number) is None:
 		return False
 	else:
 		return True

#checks if user exists in users DB
def userExists(user_name):
	if User.objects(name = user_name) is None:
		return False
	else:
		return True

def guessExists(g_id):
    if Message.objects(guess_id = g_id) is None:
        return False
    else:
        return True


#process the text if the user exists in our db
def processExisting(body, number):

    # if this looks like a message
    if parse.validMessageRequest(body):

        user_name = parse.getMessageTo(body)
        message_body = parse.getMessageBody(body)

        # this is a valid message, so we will set up a message db entry
        new_message = Message()
        new_message.from_name = User.objects(phone = number).get().name
        new_message.from_phone = number
        new_message.message = message_body
        new_message.to_name = user_name
        new_message.to_phone = ''
        g_id = str(random.randint(1,99999))  # we sms g_id out so people can guess!
        new_message.guess_id = g_id

        # if we know tagged user, we will forward the text body
        if userExists(user_name):
            # store our phone number
            to_number = (User.objects(name = user_name)).get().phone
            new_message.to_phone = to_number

            message_and_id = message_body + " (" + g_id + ")"
            
            # send the text! 
            client.sms.messages.create(to=to_number, from_="+13602052266", body=message_and_id)

        new_message.save()

    # if this looks like a guess
    elif parse.validGuessRequest(body):

        # we grab the guess the user sends us
        guess_number = parse.getGuessNumber(body)

        # if it does then we that actual name
        actual_name = Message.objects(guess_id = guess_number).get().from_name
        guess_name = parse.getGuessName(body)
        
        if (guess_name == actual_name):
            to_number = number
            message_body = "Yep. You guessed it."
            client.sms.messages.create(to=to_number, from_="+13602052266", body=message_body)
        else:
            to_number = number
            message_body = "Nope, you guessed wrong."
            client.sms.messages.create(to=to_number, from_="+13602052266", body=message_body)


    elif parse.validSignupRequest(body):
        print "yes this is true"
        to_number = number
        the_person = User.objects(phone = number).get().name
        message_body = "It seems like you are already signed up ?"
        client.sms.messages.create(to=to_number, from_="+13602052266", body=message_body)


    # if parse.validStopRequest(body):
    #     # removed from db


# def processNew(body, number):
#     if parse.validSignupRequest(body):
#         new_name = parse.getSignupName(body)
#         # add new_name with "number" (above) to db

#         # send welcome text
#     else:
#         # reply: please sign up





#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

