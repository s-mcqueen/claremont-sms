import os
from flask import Flask, request, redirect, render_template, session, url_for
import twilio.twiml
import urllib
import json
import datetime
#importing parse.py for text parsing
#import parse
#import mongodb stuff
from mongokit import Connection, Document, ObjectId

twilio_id = "AC65492579e6a94943a72ebed4c4f4b788"
twilio_token = "81ebc16c6a6fd61bf25631ee0b649e01"

app = Flask(__name__)

#connect to our mongo server (local)
connection = Connection('localhost', 27017)

#class to hold the message fields
class Message(Document):

	structure = {
		'from_name' : basestring,
		'from_phone' : basestring,
		'message' : basestring,
		'to_name' : basestring,
		'created_at': datetime.datetime
	}

	#make created_at get filled automatically
	default_values = {'created_at': datetime.datetime.utcnow}
	use_dot_notation = True

#class to hold the user fields
class Users(Document):

	structure = {
		'name' : basestring,
		'phone' : basestring,
		'created_at': datetime.datetime
	}

	#make created_at get filled automatically
	default_values = {'created_at': datetime.datetime.utcnow}
	use_dot_notation = True

#opening up a connection with mongo for message structure
connection.register([Message])
collection_message = connection['claremont-sms'].entries

#opening up a connection with mongo for user structure
connection.register([Users])
collection_users = connection['claremont-sms'].entries

#method to recieve texts, parse them, and store in mongo
@app.route("/", methods = ['GET', 'POST'])
def receive(): 
	#store the text body and phone num
    body = request.values.get('Body')
    number = request.values.get('From')

    '''TODO: add in parsing logic'''

    #store the name and phone in Users
    
    new_user = collection_users.Users()
    new_user.name = str(body)
    new_user.phone = str(number)

    print "name: " + new_user.name

    #save data in user collection
    new_user.save()

    #sends back a text
    resp = twilio.twiml.Response()
    resp.sms(body)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)














