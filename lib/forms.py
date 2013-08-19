# this class is used to control the form flow and raise
# validation errors if necessary
from send import send_verif, send_welcome
from models import user_exists, number_exists, get_verif, set_verif
from wtforms import Form, BooleanField, TextField, validators, ValidationError
from parse import format_text

#---------------------------------------------
# form processing
# --------------------------------------------

def process_web_signup(name, number):
    # generate random verif_code
    verif_code = randint(100000,999999)
    number = "+1" + number

    # if user exists (but in not active), update verif
    if user_exists(parse.format_text(name)):
        set_verif(number, verif_code)
    else:
        # store user in db, delete if verif is wrong
        create_user(name, number)
        set_verif(number, verif_code)

    # send the user an SMS with the verif_code
    send_verif(number, verif_code)

def process_verif(number):
		set_active(number)
		send_welcome(number)

#---------------------------------------------
# form validation methods
# --------------------------------------------

def validate_signup(data):
	''' validates a user signup action'''

	user = data['user']
	number = data['number']

	# form helper methods
	_must_be_first_last(user)
	_must_be_valid_number(number)
	_user_must_not_exist(user)
	_number_must_not_exist(number)

def validate_verif(data):
	''' returns true if verification code is legit '''

	number = "+1" + data['number']
	verif_code = int(data['verif'])
	correct_verif = get_verif(number)

	if verif_code != correct_verif:     
		raise ValidationError('Verification code is incorrect. Try again?')


#---------------------------------------------
# private form helper methods
# --------------------------------------------

def _must_be_first_last(user):
	''' ensures name is in format "first last" '''
	
	name_arr = user.split(" ", 1)
	
	if len(name_arr) != 2:
		raise ValidationError('Name must be include a first and last name.')

def _must_be_valid_number(number):
	''' ensures phone number is 10 digits long '''

	if len(number) != 10:
		raise ValidationError('Phone number must be 10 digits long.')

def _user_must_not_exist(user):
	''' ensures name doesn't already exist in db '''

	user = format_text(user)

	if user_exists(user):
		raise ValidationError('This name has already been taken.')

def _number_must_not_exist(number):
	''' ensures name doesn't already exist in db '''

	# add +1 at beginning number
	number = "+1" + number

	if number_exists(number):
		raise ValidationError('This phone number has already been taken.')

