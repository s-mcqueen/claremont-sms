import os
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory
import twilio.twiml
from twilio.rest import TwilioRestClient
import urllib
import json
import datetime
import random
from tokens import TWILIO_ID, TWILIO_TOKEN, TWILIO_NUM
import parse # collection of methods for text parsing

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)

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

class Message(db.DynamicDocument):
    '''class to hold the message fields'''
    from_name = db.StringField(max_length=255)
    from_phone = db.StringField(max_length=15)
    message = db.StringField(max_length=400)
    to_name = db.StringField(max_length=255)
    to_phone = db.StringField(max_length=15)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    guess_id = db.StringField(max_length=5) 

class User(db.DynamicDocument):
    '''class to hold the user fields'''
    name = db.StringField(max_length=255, unique=True)
    phone = db.StringField(max_length=15, unique=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    # guess_counter = db.StringField(max_length=5)
    
#---------------------------------------------
# controllers
# --------------------------------------------

@app.route("/", methods = ['GET'])
def display():
    messages = list(Message.objects())
    return render_template('index.html', posts = messages)
    
@app.route("/receive", methods = ['GET', 'POST'])
def receive(): 
    '''method to recieve texts, parse them, and store in mongo'''

	#store the text body and phone number
    body = request.values.get('Body')
    number = request.values.get('From')
    
    if numberExists(number):
        processExisting(body, number)

    else:
        processNew(body, number)

def numberExists(phone_number):
    '''checks if number exists in users db'''
    try:
        user = User.objects(phone = phone_number).get()
    except Exception, e:
        return False
    else:
        return True

def userExists(user_name):
    '''check if user name exists in users db'''
    try:
        user = User.objects(name = user_name).get()
    except Exception, e:
        return False
    else:
        return True

def processExisting(body, number):
    '''process the text if the user exists in our db'''

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
            to_number = User.objects(name = user_name).get().phone
            new_message.to_phone = to_number

            message_and_id = message_body + " (" + g_id + ")"
            
            # send the text! 
            client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_and_id)

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
            client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)
        else:
            to_number = number
            message_body = "Nope, you guessed wrong."
            client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


    elif parse.validSignupRequest(body):
        to_number = number
        the_user = User.objects(phone = number).get().name
        message_body = "The phone number is already registered!"
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


    elif parse.validStopRequest(body):
        # delete the user from our database
        User.objects(phone = number).get().delete()

    else:
        to_number = number
        message_body = "Text 'STOP CLAREMONT SMS' to leave the service. \
                        Text 'Firstname Lastname: message' to text a friend." 
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)



def processNew(body, number):
    if parse.validSignupRequest(body):
        new_name = parse.getSignupName(body)

        user = User()
        user.name = new_name
        user.phone = number
        user.save()

        to_number = number
        message_body = "Welcome! Text 'STOP CLAREMONT SMS' to leave the service. \
                        Text 'Firstname Lastname: message' to text a friend." 
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)

    else:
        to_number = number
        message_body = "Text 'SIGNUP: Firstname Lastname' to join Claremont SMS!" 
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

