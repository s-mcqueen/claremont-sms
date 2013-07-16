from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
from models import Message as Message
from models import User as User
from models import numberExists, userExists
from lib import forms, process

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
    ''' sends the user a verif_code and stores their info with is_active = false'''

    if request.method == "POST":
        data = request.form               
        process.processWebSignup(data['user'], data['number'])          
        return jsonify(data)


@app.route("/send_welcome", methods = ['POST'])
def sendWelcome():
    ''' sends the user a the welcome message if they enter a correct verif code'''

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
    dif = datetime.datetime.utcnow() - created_at

    if dif <= datetime.timedelta(seconds = 60):
        return "%d second%s ago" % (dif.seconds, "s"[dif.seconds==1:])
    elif dif <= datetime.timedelta(minutes = 60):
        return "%d minute%s ago" % (dif.minutes, "s"[dif.minutes==1:])
    elif dif <= datetime.timedelta(minutes = 1440):
        return "%d hour%s ago" % (dif.hours, "s"[dif.hours==1:])
    else:
        return "%d day%s ago" % (dif.days, "s"[dif.days ==1:])