import os
from flask import Flask, request, redirect
import twilio.twiml

twilio_id = "AC65492579e6a94943a72ebed4c4f4b788"
twilio_token = "81ebc16c6a6fd61bf25631ee0b649e01"

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def hello():
    ''' test '''
    body = request.values.get('Body')
    resp = twilio.twiml.Response()
    resp.sms(body)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
