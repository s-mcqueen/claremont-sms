import os

from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
import urllib
import urllib2
import json
from lib import forms # class to instantiate form object + validations
import pdb

from app import app
from lib import process
from models import Message

#---------------------------------------------
# controllers
# --------------------------------------------

@app.route("/", methods = ['GET','POST'])
def display():
    ''' displays messages and processes signup form '''

    messages = list(Message.objects())
    users = list(User.objects())

    # combine messages and users, order by date
    posts = messages + users
    posts.sort(key=lambda x: x.created_at, reverse = True)

    # convert created_at to a format we care about
    for x in xrange(len(posts)):
        posts[x].created_at = convertDate(posts[x].created_at)

    return render_template('index.html', posts = posts)


@app.route("/signup", methods = ['POST'])
def signup():
    ''' receives signup form data from the homepage signup form and checks for errors '''

    if request.method == "POST":
        data = request.form        
       
        try:
            forms.validateSignup(data)
        except ValidationError, e:
            errors_dict = {}
            errors_dict['errors'] = e.message
            return jsonify(errors_dict)            
        else:            
            return jsonify(data)


@app.route("/send_verif", methods = ['POST'])
def sendVerif():
    ''' launched on verif modal open, sends the user a verif_code and stores their info '''

    if request.method == "POST":
        data = request.form               
        processWebSignup(data['user'], data['number'])          
        return jsonify(data)


@app.route("/send_welcome", methods = ['POST'])
def sendWelcome():
    ''' launched on into modal open, sends the user a the welcome message '''

    if request.method == "POST":
        data = request.form 

        # deprecated function
        sendWelcome(data['number'])          
        return jsonify(data)      


@app.route("/receive_verif", methods = ['POST'])
def receiveVerif():
    ''' receives verif form data from the verif modal and processes it '''

    if request.method == "POST":
        data = request.form

        try:
            forms.validateVerif(data)
        except ValidationError, e:
            errors_dict = {}
            errors_dict['errors'] = e.message
            deleteUser(data['number'])
            return jsonify(errors_dict)            
        else:            
            setActive(data['number'])            
            return jsonify(data)

    
@app.route("/receive_text", methods = ['GET', 'POST'])
def receiveText(): 
    ''' method to recieve texts, parse them, and store in mongo'''

    #store the text body and phone number
    body = request.values.get('Body')
    number = request.values.get('From')
    
    if numberExists(number):
        processExisting(body, number)

    else:
        processNew(body, number)


def convertDate(created_at):
    dif = datetime.utcnow() - created_at

    if dif <= timedelta(seconds = 60):
        return "%d second%s ago" % (dif.seconds, "s"[dif.seconds==1:])
    elif dif <= timedelta(minutes = 60):
        return "%d minute%s ago" % (dif.minutes, "s"[dif.minutes==1:])
    elif dif <= timedelta(minutes = 1440):
        return "%d hour%s ago" % (dif.hours, "s"[dif.hours==1:])
    else:
        return "%d day%s ago" % (dif.days, "s"[dif.days ==1:])


#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

