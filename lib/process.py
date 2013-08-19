import parse
from random import random, randint
from send import send_welcome, send_message_and_id, send_guess_success, send_guess_failure, \
                 send_already_signed_up, send_invalid, send_signup_request
from models import create_user, create_message, number_exists, user_exists, set_verif, get_number_from_name, \
                   get_name_from_number, get_name_from_guess_id
from app import app

#---------------------------------------------
# SMS processing
# --------------------------------------------  

def process_existing(body, number):
    ''' process a text if the user does exist in the db'''    

    # looks like a message
    if parse.valid_message_request(body):
        _process_valid_message(body, number)

    # looks like a guess
    elif parse.valid_guess_request(body):
        _process_valid_guess(body, number)

    # looks like a signup request
    elif parse.valid_signup_request(body):
        _process_valid_signup(body, number)

    # looks like a stop request
    elif parse.valid_stop_request(body):
        delete_user(number)

    # looks like some garbage we cant parse
    else:
        send_invalid(number)

def process_new(body, number):
    ''' process a text if the user does NOT exist in the db '''

    # looks like a signup request
    if parse.valid_signup_request(body):
        new_name = parse.get_signup_name(body)
        create_user(new_name, number)
        send_welcome(number)
    
    # looks like anything else
    else:
        send_signup_request(number)

#---------------------------------------------
# private helper methods
# --------------------------------------------  

def _process_valid_message(body, number):
    from_name = get_name_from_number(number)
    from_phone = number
    message_body = parse.get_message_body(body)
    to_name = parse.get_message_to(body)
    # TODO: not random ID
    guess_id = str(random.randint(1,99999))  # we sms g_id out so people can guess!

    # if we know tagged user, we will forward the text body
    if user_exists(user_name):
        to_phone = get_number_from_name(user_name)
        create_message(from_name, from_phone, message_body, to_name, to_phone, guess_id)        
        send_message_and_id(message_body, guess_id, to_number) # send the text! 
    # user doesn't exist but we save the message body anyway
    else:
        to_phone = ''
        create_message(from_name, from_phone, message_body, to_name, to_phone, guess_id)


def _process_valid_guess(body, number):
    # we grab the guess the user sends us
    guess_number = parse.get_guess_number(body)

    # if it does then we that actual name
    actual_name = get_name_from_guess_id()
    guess_name = parse.get_guess_name(body)
    
    if (guess_name == actual_name):        
        send_guess_success(to_number)        
    else:
        send_guess_failure(to_number)


def _process_valid_signup(body, number):    
    if number_exists(number):
        send_already_signed_up(tnumber)
    else:
        send_signup_request(number)    




