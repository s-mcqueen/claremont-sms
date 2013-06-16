import re

#---------------------------------------------
# helper methods
# --------------------------------------------

def colonSplit(sms_body):
    ''' helper function that splits strings '''
    
    return sms_body.split(":", 1) # split on the first ":"

def formatText(sms_body):
    ''' helper function that removes spaces and formats
        to lower case'''

    return sms_body.lower().replace(' ', '')

#---------------------------------------------
# message validity
# --------------------------------------------

def validMessageRequest(sms_body):
    ''' return true if sms is formatted like a message 
        ie: "first last: message goes here '''

    sms = colonSplit(sms_body)
    if (len(sms) < 2):
        # there is no colon
        return False
    
    name = formatText(sms[0])

    # only return true if name_section only has letters
    for c in name:
        if c not in 'qwertyuiopasdfghjklzxcvbnm':
            return False

    if (name == 'signup'):
        return False

    return True

def getMessageTo(sms_body):
    ''' this should NOT be called unless validMessageRequest
        has returned True '''

    sms = colonSplit(sms_body)
    name = formatText(sms[0])
   
    return name

def getMessageBody(sms_body):
    ''' this should NOT be called unless validMessageRequest
        has returned True '''

    sms = colonSplit(sms_body)
    message = sms[1]

    return message

#---------------------------------------------
# guess validity
# --------------------------------------------

def validGuessRequest(sms_body):
    ''' returns true if the sms is formatted like a guess
        ie: "23: first last" '''

    sms = colonSplit(sms_body)

    if (len(sms) < 2):
        # there is no colon
        return False

    guess = formatText(sms[0])

    # only return true if guess_section only has digits
    for c in guess:
        if c not in '1234567890':
            return False

    return True

def getGuessNumber(sms_body):
    ''' this should NOT be called unless validGuessRequest
        has returned True '''

    sms = colonSplit(sms_body)
    guess_number = sms[0].replace(' ', '')
   
    return guess_number

def getGuessName(sms_body):
    ''' this should NOT be called unless validGuessRequest
        has returned True '''

    sms = colonSplit(sms_body)
    guess_name = formatText(sms[1])

    return guess_name


#---------------------------------------------
# sign up validity
# --------------------------------------------

def validSignupRequest(sms_body):
    ''' return true if the sms is a valid signup request
        ie: "SIGNUP: first last" '''

    sms = colonSplit(sms_body)

    if (len(sms) < 2):
        # there is no colon, so we don't have a name
        return False

    signup_phrase = formatText(sms[0])

    if (signup_phrase == 'signup'):
        return True
    return False

def getSignupName(sms_body):
    ''' this should NOT be called unless validSignupRequest
        has returned True '''    

    sms = colonSplit(sms_body)
    signup_name = sms[1].lower().replace(' ', '')

    # make name lower case and remove spaces   
    return signup_name

#---------------------------------------------
# stop validity
# --------------------------------------------

def validStopRequest(sms_body):
    ''' return true if the sms_body  '''

    # lower case and no spaces
    stop_phrase = sms_body.lower().replace(' ', '')

    if (stop_phrase == "stopclaremontsms"):
        return True
    else:
        return False

