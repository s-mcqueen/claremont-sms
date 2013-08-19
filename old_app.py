# import urllib2
# import json
# from tokens import TWILIO_ID, TWILIO_TOKEN, TWILIO_NUM
# import parse # collection of methods for text parsing
# import forms # class to instantiate form object + validations
# import pdb
# from wtforms import ValidationError
# from random import random, randint
# from multiprocessing import Process
# from datetime import datetime, timedelta
# #---------------------------------------------
# # initialization
# # --------------------------------------------

# import os
# from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
# import twilio.twiml
# from twilio.rest import TwilioRestClient

# app = Flask(__name__)
# app.config.update(
#     DEBUG = True,
# )
# app.config.from_object('config')

# client = TwilioRestClient(TWILIO_ID, TWILIO_TOKEN)

# #---------------------------------------------
# # database
# # --------------------------------------------

# from mongoengine import connect
# from flask.ext.mongoengine import MongoEngine

# DB_NAME = 'claremont-sms-db'
# DB_USERNAME = 'evan'
# DB_PASSWORD = 'smegma69'
# DB_HOST_ADDRESS = 'ds031857.mongolab.com:31857/claremont-sms-db'

# app.config["MONGODB_DB"] = DB_NAME 
# connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
# db = MongoEngine(app)

# #---------------------------------------------
# # models
# # --------------------------------------------

# class Message(db.DynamicDocument):

#     from_name = db.StringField(max_length=255)
#     from_phone = db.StringField(max_length=15)
#     message = db.StringField(max_length=400)
#     to_name = db.StringField(max_length=255)
#     to_phone = db.StringField(max_length=15)
#     created_at = db.DateTimeField(default=datetime.utcnow())
#     guess_id = db.StringField(max_length=5) 

# class User(db.DynamicDocument):

#     name = db.StringField(max_length=255, unique=True)
#     phone = db.StringField(max_length=15, unique=True)
#     created_at = db.DateTimeField(default=datetime.utcnow())
#     verif_code = db.IntField()
#     is_active = db.BooleanField(default=False)
#     # guess_counter = db.StringField(max_length=5)
    
# #---------------------------------------------
# # controllers
# # --------------------------------------------

# @app.route("/", methods = ['GET','POST'])
# def display():
#     ''' displays messages and processes signup form '''

#     messages = list(Message.objects())
#     users = list(User.objects())

#     # combine messages and users, order by date
#     posts = messages + users
#     posts.sort(key=lambda x: x.created_at, reverse = True)

#     # convert created_at to a format we care about
#     for x in xrange(len(posts)):
#         posts[x].created_at = convertDate(posts[x].created_at)

#     return render_template('index.html', posts = posts)


# @app.route("/signup", methods = ['POST'])
# def signup():
#     ''' receives signup form data from the homepage signup form and checks for errors '''

#     if request.method == "POST":
#         data = request.form        
       
#         try:
#             forms.validateSignup(data)
#         except ValidationError, e:
#             errors_dict = {}
#             errors_dict['errors'] = e.message
#             return jsonify(errors_dict)            
#         else:            
#             return jsonify(data)


# @app.route("/send_verif", methods = ['POST'])
# def sendVerif():
#     ''' launched on verif modal open, sends the user a verif_code and stores their info '''

#     if request.method == "POST":
#         data = request.form               
#         process_web_signup(data['user'], data['number'])          
#         return jsonify(data)

# @app.route("/send_welcome", methods = ['POST'])
# def sendWelcome():
#     ''' launched on into modal open, sends the user a the welcome message '''

#     if request.method == "POST":
#         data = request.form               
#         sendWelcome(data['number'])          
#         return jsonify(data)        


# @app.route("/receive_verif", methods = ['POST'])
# def receiveVerif():
#     ''' receives verif form data from the verif modal and processes it '''

#     if request.method == "POST":
#         data = request.form

#         try:
#             forms.validateVerif(data)
#         except ValidationError, e:
#             errors_dict = {}
#             errors_dict['errors'] = e.message
#             delete_user(data['number'])
#             return jsonify(errors_dict)            
#         else:            
#             setActive(data['number'])            
#             return jsonify(data)

    
# @app.route("/receive_text", methods = ['GET', 'POST'])
# def receiveText(): 
#     ''' method to recieve texts, parse them, and store in mongo'''

# 	#store the text body and phone number
#     body = request.values.get('Body')
#     number = request.values.get('From')
    
#     if number_exists(number):
#         process_existing(body, number)

#     else:
#         process
process_new(body, number)

# #---------------------------------------------
# # SMS processing
# # --------------------------------------------

# def number_exists(phone_number):
#     ''' checks if number exists in users db'''

#     try:
#         user = User.objects(phone = phone_number).get()
#     except Exception, e:
#         return False
#     else:
#         return True

# def user_exists(user_name):
#     ''' check if user name exists in users db'''

#     try:
#         user = User.objects(name = user_name).get()
#     except Exception, e:
#         return False
#     else:
#         return True

# def process_existing(body, number):
#     ''' process the text if the user exists in our db'''

#     # if this looks like a message
#     if parse.validMessageRequest(body):

#         user_name = parse.get_message_to(body)
#         message_body = parse.get_message_body(body)

#         # this is a valid message, so we will set up a message db entry
#         new_message = Message()
#         new_message.from_name = User.objects(phone = number).get().name
#         new_message.from_phone = number
#         new_message.message = message_body
#         new_message.to_name = user_name
#         new_message.to_phone = ''
#         g_id = str(random.randint(1,99999))  # we sms g_id out so people can guess!
#         new_message.guess_id = g_id

#         # if we know tagged user, we will forward the text body
#         if user_exists(user_name):
#             # store our phone number
#             to_number = User.objects(name = user_name).get().phone
#             new_message.to_phone = to_number

#             message_and_id = message_body + " (" + g_id + ")"
            
#             # send the text! 
#             client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_and_id)

#         new_message.save()

#     # if this looks like a guess
#     elif parse.valid_guess_request(body):

#         # we grab the guess the user sends us
#         guess_number = parse.get_guess_number(body)

#         # if it does then we that actual name
#         actual_name = Message.objects(guess_id = guess_number).get().from_name
#         guess_name = parse.get_guess_name(body)
        
#         if (guess_name == actual_name):
#             to_number = number
#             message_body = "Yep. You guessed it."
#             client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)
#         else:
#             to_number = number
#             message_body = "Nope, you guessed wrong."
#             client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


#     elif parse.valid_signup_request(body):
#         to_number = number
#         the_user = User.objects(phone = number).get().name
#         message_body = "The phone number is already registered!"
#         client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


#     elif parse.valid_stop_request(body):
#         # delete the user from our database
#         User.objects(phone = number).delete()

#     else:
#         sendWelcome(number)


# def process
process_new(body, number):
#     if parse.valid_signup_request(body):
#         new_name = parse.get
get_signup_name(body)

#         user = User()
#         user.name = new_name
#         user.phone = "+1" + number
#         user.save()

#         sendWelcome(number)
#     else:
#         requestSignup(number)

# #---------------------------------------------
# # outgoing SMS helpers
# # --------------------------------------------

# def requestSignup(number):
#     message_body = "Text 'SIGNUP: Firstname Lastname' to join Claremont SMS!" 
#     client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)

# def sendWelcome(number):
#     message_body = "Welcome! Text 'STOP CLAREMONT SMS' to leave the service. \
#                         Text 'Firstname Lastname: message' to text a friend." 
#     client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)

# def sendVerif(number, verif_code):
#     message_body = "Hello from Claremont SMS! Enter %d on the sign up page to verify your account." % verif_code
#     client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)

# #---------------------------------------------
# # web signup processing
# # --------------------------------------------
       
# def process_web_signup(name, number):
#     # generate random verif_code
#     verif_code = randint(100000,999999)

#     # check if user already exists
#     if user_exists(parse.format_text(name)):
#         number = "+1" + number
#         user = User.objects(phone = number)
#         user.update(set__verif_code = verif_code)

#     else:
#         # store user in db, delete if verif is wrong
#         user = User()
#         user.name = parse.format_text(name)
#         user.phone = "+1" + number
#         user.verif_code = verif_code
#         user.save()

#     sendVerif(number, verif_code)


# def delete_user(number):
#     User.objects(phone = number).delete()

# def setActive(number):
#     number = "+1" + number
#     user = User.objects(phone = number)
#     user.update(set__is_active = True)

# #---------------------------------------------
# # more helpers
# # --------------------------------------------

# def convertDate(created_at):
#     dif = datetime.utcnow() - created_at

#     if dif <= timedelta(seconds = 60):
#         return "%d second%s ago" % (dif.seconds, "s"[dif.seconds==1:])
#     elif dif <= timedelta(minutes = 60):
#         return "%d minute%s ago" % (dif.minutes, "s"[dif.minutes==1:])
#     elif dif <= timedelta(minutes = 1440):
#         return "%d hour%s ago" % (dif.hours, "s"[dif.hours==1:])
#     else:
#         return "%d day%s ago" % (dif.days, "s"[dif.days ==1:])

# #---------------------------------------------
# # launch
# # --------------------------------------------

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)

