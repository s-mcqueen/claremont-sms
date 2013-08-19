from app import app
#---------------------------------------------
# SMS copy
# --------------------------------------------

GUESS_SUCCESS = "Yep. You guessed it."
GUESS_FAILURE = "Nope, you guessed wrong."
ALREADY_SIGNEDUP = "The phone number is already registered!"
INVALID_TEXT = "Text 'STOP CLAREMONT SMS' to leave the service. \
                Text 'Firstname Lastname: message' to text a friend." 
WELCOME = "Welcome! Text 'STOP CLAREMONT SMS' to leave the service. \
            Text 'Firstname Lastname: message' to text a friend."
REQUEST_SIGNUP = "Text 'SIGNUP: Firstname Lastname' to join Claremont SMS!"

def send_welcome(number):		
		client.sms.messages.create(to=number, from_=TWILIO_NUM, body=WELCOME)

def send_verif(number, verif_code):
		message_body = "Hello from Claremont SMS! Enter %d on the sign up page to verify your account." % verif_code
		client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)

def send_message_and_id(message_body, guess_id, tnumber):
		message_and_id = message_body + " (" + guess_id + ")"
		client.sms.messages.create(to=tnumber, from_=TWILIO_NUM, body=message_and_id)

def send_guess_success(number):		
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=GUESS_SUCCESS)

def send_guess_failure(number):
		client.sms.messages.create(to=number, from_=TWILIO_NUM, body=GUESS_FAILURE)

def send_already_signed_up(number):
		client.sms.messages.create(to=number, from_=TWILIO_NUM, body=ALREADY_SIGNEDUP)

def send_invalid(number):
		client.sms.messages.create(to=number, from_=TWILIO_NUM, body=INVALID_TEXT)

def send_signup_request(number):	    
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=REQUEST_SIGNUP)
