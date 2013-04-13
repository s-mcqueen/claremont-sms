import tokens
import flask from Flask, request, redirect
import twilio.twiml

app = Flask

@app.route("/", methods = ['GET', 'POST'])
def hello():
    ''' test '''
    body = request.values.get('body')
    resp = twilio.twiml.Response()
    resp.sms(body)
    return str(resp)

if __name__ == "__main__":
    app.run(debug = True)
