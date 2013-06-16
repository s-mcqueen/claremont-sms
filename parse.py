import re

#---------------------------------------------
# helper methods
# --------------------------------------------

def colonSplit(sms_body):
    ''' helper function that splits strings '''
    return sms_body.split(":", 1) # split on the first ":"

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
    
    name_section = sms[0]

    # make name lower case and remove spaces
    name_section = name_section.lower().replace(' ', '')

    # only return true if name_section only has letters
    for c in name_section:
        if c not in 'qwertyuiopasdfghjklzxcvbnm':
            return False

    if (name_section == 'signup'):
        return False

    return True

def getMessageTo(sms_body):
    ''' this should NOT be called unless validMessageRequest
        has returned True '''

    sms = colonSplit(sms_body)
    name_section = sms[0]
   
    # make name lower case and remove spaces
    name_section = name_section.lower().replace(' ', '')
    return name_section

def getMessageBody(sms_body):
    ''' this should NOT be called unless validMessageRequest
        has returned True '''
    sms = colonSplit(sms_body)
    message_section = sms[1]
    return message_section

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
    guess_section = sms[0]

    # make name lower case and remove spaces
    guess_section = guess_section.replace(' ', '')

    # only return true if guess_section only has digits
    for c in guess_section:
        if c not in '1234567890':
            return False

    return True

def getGuessNumber(sms_body):
    ''' this should NOT be called unless validGuessRequest
        has returned True '''
    sms = colonSplit(sms_body)
    guess_section = sms[0]
   
    # remove spaces
    guess_section = guess_section.replace(' ', '')
    return guess_section

def getGuessName(sms_body):
    ''' this should NOT be called unless validGuessRequest
        has returned True '''
    sms = colonSplit(sms_body)
    name_section = sms[1].lower().replace(' ', '')

    return name_section


#---------------------------------------------
# sign up validity
# --------------------------------------------

def validSignupRequest(sms_body):
    ''' return true if the sms is a valid signup request
        ie: "SIGNUP: first last" '''
    sms = colonSplit(sms_body)
    signup_phrase = sms[0].lower().replace(' ', '')

    if (len(sms) < 2):
        # there is no colon, so we don't have a name
        return False

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

