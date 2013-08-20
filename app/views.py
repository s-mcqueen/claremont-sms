from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
from wtforms import Form, BooleanField, TextField, validators, ValidationError
from models import get_message_list, get_user_list, number_exists, user_exists, delete_user
from lib import forms, process
from app import app
import pdb

#---------------------------------------------
# web controller actions
# --------------------------------------------

@app.route("/", methods = ['GET','POST'])
def display():
    ''' displays messages and processes signup form '''
    messages = get_message_list()
    users = get_user_list()

    # combine messages and users, order by date
    posts = messages + users
    posts.sort(key=lambda x: x.created_at, reverse = True)

    # convert created_at to a format we care about
    for x in xrange(len(posts)):
        posts[x].created_at = _convert_date(posts[x].created_at)

    return render_template('index.html', posts = posts)


@app.route("/signup", methods = ['POST'])
def signup():
    ''' receives signup form data from the homepage signup form 
        and checks for errors '''
    if request.method == "POST":
        data = request.form        
       
        try:
            forms.validate_signup(data)
        except ValidationError, e:
            errors_dict = {}
            errors_dict['errors'] = e.message
            return jsonify(errors_dict)            
        else:            
            return jsonify(data)


@app.route("/send_verif", methods = ['POST'])
def send_verif():
    ''' sends the user a verif_code and stores their info with 
        is_active = false'''
    if request.method == "POST":
        data = request.form               
        forms.process_web_signup(data['user'], data['number'])          
        return jsonify(data)  


@app.route("/receive_verif", methods = ['POST'])
def receive_verif():
    ''' receives verif form data from the verif modal and processes it '''
    if request.method == "POST":
        data = request.form

        try:
            forms.validate_verif(data)
        except ValidationError, e:
            errors_dict = {}
            errors_dict['errors'] = e.message
            delete_user(data['number'])
            return jsonify(errors_dict)            
        else:            
            forms.process_verif(data['number'])            
            return jsonify(data)

#---------------------------------------------
# SMS controller
# --------------------------------------------
    
@app.route("/receive_text", methods = ['GET', 'POST'])
def receive_text(): 
    ''' method to recieve texts, parse them, and store in mongo'''

    # store the text body and phone number
    body = request.values.get('Body')
    number = request.values.get('From')
    
    if number_exists(number):
        process.process_existing(body, number)
    else:
        process.process_new(body, number)

#---------------------------------------------
# private helper methods
# --------------------------------------------  

def _convert_date(created_at):
    dif = datetime.now() - created_at    

    if dif <= timedelta(microseconds = 1000000)
        return "0 seconds ago"
    elif dif <= timedelta(seconds = 60):
        return "%d second%s ago" % (dif.seconds, "s"[dif.seconds==1:])
    elif dif <= timedelta(minutes = 60):
        return "%d minute%s ago" % (dif.minutes, "s"[dif.minutes==1:])
    elif dif <= timedelta(hours = 24):
        return "%d hour%s ago" % (dif.hours, "s"[dif.hours==1:])
    else:
        return "%d day%s ago" % (dif.days, "s"[dif.days ==1:])