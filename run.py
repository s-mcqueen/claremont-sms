import os

from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
import urllib
import urllib2
import json
from lib import forms # class to instantiate form object + validations
import pdb

from app import app
from lib import process
# from models import Message

#---------------------------------------------
# controllers
# --------------------------------------------

@app.route("/", methods = ['GET','POST'])
def display():
    ''' displays messages and processes signup form '''

    # messages = list(Message.objects())
    # form = forms.SignupForm()

    # if form.validate_on_submit():
    #     number = "+1" + form.number.data
    #     process.requestSignup(number)
    #     return redirect("/")

    # return render_template('index.html', posts = messages, form = form)
    return render_template('index.html')

# @app.route("/signup", methods = ['GET','POST'])
# def signup():
#     ''' recieves signup form data via an ajax POST request '''

#     if request.method == "POST":
#         data = request.form
#         signup_str = 'SIGNUP: %s' % data['user']
#         process.processNew(signup_str, data['number'])
#         return jsonify(data)

    
# @app.route("/receive", methods = ['GET', 'POST'])
# def receive(): 
#     ''' method to recieve texts, parse them, and store in mongo'''

# 	#store the text body and phone number
#     body = request.values.get('Body')
#     number = request.values.get('From')
    
#     if numberExists(number):
#         process.processExisting(body, number)

#     else:
#         process.processNew(body, number)


#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

