import re

#---------------------------------------------
# SMS message validity
# --------------------------------------------

def valid_message_request(sms_body):
    ''' return true if sms is formatted like a message 
        ie: "first last: message goes here '''

    sms = colon_split(sms_body)
    if (len(sms) < 2):
        # there is no colon
        return False
    
    name = format_text(sms[0])

    # only return true if name_section only has letters
    for c in name:
        if c not in 'qwertyuiopasdfghjklzxcvbnm':
            return False

    if (name == 'signup'):
        return False

    return True

def get_message_to(sms_body):
    ''' this should NOT be called unless valid_message_request
        has returned True '''

    sms = colon_split(sms_body)
    name = format_text(sms[0])
   
    return name

def get_message_body(sms_body):
    ''' this should NOT be called unless valid_message_request
        has returned True '''

    sms = colon_split(sms_body)
    message = sms[1]

    return message

#---------------------------------------------
# SMS guess validity
# --------------------------------------------

def valid_guess_request(sms_body):
    ''' returns true if the sms is formatted like a guess
        ie: "23: first last" '''

    sms = colon_split(sms_body)

    if (len(sms) < 2):
        # there is no colon
        return False

    guess = format_text(sms[0])

    # only return true if guess_section only has digits
    for c in guess:
        if c not in '1234567890':
            return False

    return True

def get_guess_number(sms_body):
    ''' this should NOT be called unless valid_guess_request
        has returned True '''

    sms = colon_split(sms_body)
    guess_number = sms[0].replace(' ', '')
   
    return guess_number

def get_guess_name(sms_body):
    ''' this should NOT be called unless valid_guess_request
        has returned True '''

    sms = colon_split(sms_body)
    guess_name = format_text(sms[1])

    return guess_name


#---------------------------------------------
# SMS sign up validity
# --------------------------------------------

def valid_signup_request(sms_body):
    ''' return true if the sms is a valid signup request
        ie: "SIGNUP: first last" '''

    sms = colon_split(sms_body)

    if (len(sms) < 2):
        # there is no colon, so we don't have a name
        return False

    signup_phrase = format_text(sms[0])

    if (signup_phrase == 'signup'):
        return True
    return False

def get_signup_name(sms_body):
    ''' this should NOT be called unless valid_signup_request
        has returned True '''    

    sms = colon_split(sms_body)
    signup_name = format_text(sms[1])

    return signup_name

#---------------------------------------------
# SMS stop validity
# --------------------------------------------

def valid_stop_request(sms_body):
    ''' return true if the sms_body  '''

    # lower case and no spaces
    stop_phrase = format_text(sms_body)

    if (stop_phrase == "stopclaremontsms"):
        return True
    else:
        return False


#---------------------------------------------
# helper methods for text parsing
# --------------------------------------------

def colon_split(sms_body):
    ''' helper function that splits strings '''
    
    return sms_body.split(":", 1) # split on the first ":"

def format_text(sms_body):
    ''' helper function that removes spaces and formats
        to lower case'''

    return sms_body.lower().replace(' ', '')

