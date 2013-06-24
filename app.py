import os
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
import twilio.twiml
from twilio.rest import TwilioRestClient
import urllib
import urllib2
import simplejson
import json
import datetime
import random
from tokens import TWILIO_ID, TWILIO_TOKEN, TWILIO_NUM
import forms # class to instantiate form object + validations
import pdb

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)
app.config.from_object('config')

client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)

#---------------------------------------------
# database
# --------------------------------------------

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'claremont-sms-db'
DB_USERNAME = 'evan'
DB_PASSWORD = 'smegma69'
DB_HOST_ADDRESS = 'ds031857.mongolab.com:31857/claremont-sms-db'

app.config["MONGODB_DB"] = DB_NAME 
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

import process  # text processing API


#---------------------------------------------
# controllers
# --------------------------------------------

@app.route("/", methods = ['GET','POST'])
def display():
    ''' displays messages and processes signup form '''

    messages = list(Message.objects())
    form = forms.SignupForm()

    if form.validate_on_submit():
        number = "+1" + form.number.data
        process.requestSignup(number)
        return redirect("/")

    return render_template('index.html', posts = messages, form = form)

@app.route("/signup", methods = ['GET','POST'])
def signup():
    ''' recieves signup form data via an ajax POST request '''

    if request.method == "POST":
        data = request.form
        signup_str = 'SIGNUP: %s' % data['user']
        process.processNew(signup_str, data['number'])
        return jsonify(data)

    
@app.route("/receive", methods = ['GET', 'POST'])
def receive(): 
    ''' method to recieve texts, parse them, and store in mongo'''

	#store the text body and phone number
    body = request.values.get('Body')
    number = request.values.get('From')
    
    if numberExists(number):
        process.processExisting(body, number)

    else:
        process.processNew(body, number)


#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

