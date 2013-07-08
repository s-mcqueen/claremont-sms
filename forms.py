from app import Message, User, userExists, numberExists
from wtforms import Form, BooleanField, TextField, validators, ValidationError
import pdb
from parse import formatText

def validate_signup(data):
	''' validates a user signup action'''

	user = data['user']
	number = data['number']

	must_be_first_last(user)
	must_be_valid_number(number)
	user_must_not_exist(user)
	number_must_not_exist(number)

def validate_verif(data):
	''' returns true if verification code is legit '''

	number = "+1" + data['number']
	verif_code = data['verif']

	correct_verif = str(User.objects(phone = number).get().verif_code)
	if verif_code != correct_verif:
		pdb.set_trace()        
		raise ValidationError('Verification code is incorrect. Try again?')


#---------------------------------------------
# helper methods
# --------------------------------------------

def must_be_first_last(user):
	''' ensures name is in format "first last" '''
	
	name_arr = user.split(" ", 1)
	
	if len(name_arr) != 2:
		raise ValidationError('Name must be include a first and last name.')

def must_be_valid_number(number):
	''' ensures phone number is 10 digits long '''

	if len(number) != 10:
		raise ValidationError('Phone number must be 10 digits long.')

def user_must_not_exist(user):
	''' ensures name doesn't already exist in db '''

	user = formatText(user)

	if userExists(user):
		raise ValidationError('This name has already been taken.')

def number_must_not_exist(number):
	''' ensures name doesn't already exist in db '''

	# add +1 at beginning number
	number = "+1" + number

	if numberExists(number):
		raise ValidationError('This phone number has already been taken.')

