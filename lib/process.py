import parse
from models import Message
from models import User
from models import numberExists
from models import userExists

# sms copy
GUESS_SUCCESS = "Yep. You guessed it."
GUESS_FAILURE = "Nope, you guessed wrong."
ALREADY_SIGNEDUP = "The phone number is already registered!"
INVALID_TEXT = "Text 'STOP CLAREMONT SMS' to leave the service. \
                Text 'Firstname Lastname: message' to text a friend." 
WELCOME = "Welcome! Text 'STOP CLAREMONT SMS' to leave the service. \
            Text 'Firstname Lastname: message' to text a friend."
REQUEST_SIGNUP = "Text 'SIGNUP: Firstname Lastname' to join Claremont SMS!"


def processExisting(body, number):
    ''' process a text if the user does exist in the db'''

    # looks like a message
    if parse.validMessageRequest(body):
        _processValidMessage(body, number)

    # looks like a guess
    elif parse.validGuessRequest(body):
        _processValidGuess(body, number)

    # looks like a signup request
    elif parse.validSignupRequest(body):
        _processValidSignup(body, number)

    # looks like a stop request
    elif parse.validStopRequest(body):
        _processValidStop(body, number)

    # looks like some garbage we cant parse
    else:
        _processInvalidText(body, number)

# only processes text signups.
def processNew(body, number):
    ''' process a text if the user does NOT exist in the db'''

    # looks like a signup request
    if parse.validSignupRequest(body):
        new_name = parse.getSignupName(body)
        models.createUser(new_name, number)
        message_body = WELCOME 
        client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)
    
    # looks like anything else
    else:
        _requestSignup(number)


def processWebSignup(name, number):
    # generate random verif_code
    verif_code = randint(100000,999999)

    # check if user already exists
    if userExists(parse.formatText(name)):
        number = "+1" + number
        user = User.objects(phone = number)
        user.update(set__verif_code = verif_code)

    else:
        # store user in db, delete if verif is wrong
        user = User()
        user.name = parse.formatText(name)
        user.phone = "+1" + number
        user.verif_code = verif_code
        user.save()

    sendVerif(number, verif_code)


def _processValidMessage(body, number):
    from_name = User.objects(phone = number).get().name
    from_phone = number
    message_body = parse.getMessageBody(body)
    to_name = parse.getMessageTo(body)
    # TODO: not random ID
    guess_id = str(random.randint(1,99999))  # we sms g_id out so people can guess!

    # if we know tagged user, we will forward the text body
    if userExists(user_name):
        to_phone = User.objects(name = user_name).get().phone
        models.createMessage(from_name, from_phone, message_body, to_name, to_phone, guess_id)

        # send the text! 
        message_and_id = message_body + " (" + guess_id + ")"
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_and_id)

    else:
        to_phone = ''
        models.createMessage(from_name, from_phone, message_body, to_name, to_phone, guess_id)


def _processValidGuess(body, number):
    # we grab the guess the user sends us
    guess_number = parse.getGuessNumber(body)

    # if it does then we that actual name
    actual_name = Message.objects(guess_id = guess_number).get().from_name
    guess_name = parse.getGuessName(body)
    
    if (guess_name == actual_name):
        to_number = number
        message_body = GUESS_SUCCESS
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)
    else:
        to_number = number
        message_body = GUESS_FAILURE
        client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


def _processValidSignup(body, number):
    to_number = number
    the_user = User.objects(phone = number).get().name
    message_body = ALREADY_SIGNEDUP
    client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)


def _processValidStop(body, number):
    # delete the user from our database
    User.objects(phone = number).get().delete()


def _processInvalidText(body, number):
    to_number = number
    message_body = INVALID_TEXT
    client.sms.messages.create(to=to_number, from_=TWILIO_NUM, body=message_body)

       
def _requestSignup(number):
    message_body = REQUEST_SIGNUP 
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)


# helper methods, do we need these?

def requestSignup(number):
    message_body = "Text 'SIGNUP: Firstname Lastname' to join Claremont SMS!" 
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)


def sendWelcome(number):
    message_body = "Welcome! Text 'STOP CLAREMONT SMS' to leave the service. \
                        Text 'Firstname Lastname: message' to text a friend." 
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)


def sendVerif(number, verif_code):
    message_body = "Hello from Claremont SMS! Enter %d on the sign up page to verify your account." % verif_code
    client.sms.messages.create(to=number, from_=TWILIO_NUM, body=message_body)


