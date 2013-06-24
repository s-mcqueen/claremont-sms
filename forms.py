from app import Message, User, userExists, numberExists
from wtforms import Form, BooleanField, TextField, validators, ValidationError
import pdb
from parse import formatText

def validate_signup(data):
	''' calls helper methods for a user signup action'''

	user = data['user']
	number = data['number']

	must_be_first_last(user)
	must_be_valid_number(number)
	user_must_not_exist(user)
	number_must_not_exist(number)

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

