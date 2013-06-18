from flask.ext.wtf import Form, TextField
from flask.ext.wtf import Required
from app import Message, User, userExists, numberExists

def must_be_first_last(form,field):
	''' ensures name is in formart "first last" '''
	
	name_arr = field.data.split(" ", 1)
	
	if len(name_arr) != 2:
		raise ValidationError('Name must be in format "first last"')

def must_be_valid_number(form,field):
	''' ensures phone number is 10 digits long '''

	if len(field.data) != 10:
		raise ValidationError('Phone number must be 10 digits long')

def user_must_not_exist(form,field):
	''' ensures name doesn't already exist in db '''

	if userExists(field.data):
		raise ValidationError('This name has already been taken!')

def number_must_not_exist(form,field):
	''' ensures name doesn't already exist in db '''

	# add +1 at beginning number
	number = "+1" + field.data

	if numberExists(number):
		raise ValidationError('This phone number has already exists!')

class SignupForm(Form):
	user = TextField('name', validators = [Required(), must_be_first_last, user_must_not_exist])
	number = TextField('number', validators = [Required(), must_be_valid_number, number_must_not_exist])

