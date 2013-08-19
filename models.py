import datetime
from app import db

#---------------------------------------------
# model class schema
# --------------------------------------------

class Message(db.DynamicDocument):
    ''' class to hold the message fields'''
    from_name = db.StringField(max_length=255)
    from_phone = db.StringField(max_length=15)
        
    message_body = db.StringField(max_length=400)
    to_name = db.StringField(max_length=255)
    to_phone = db.StringField(max_length=15)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    guess_id = db.StringField(max_length=5) 


class User(db.DynamicDocument):
    ''' class to hold the user fields'''
    name = db.StringField(max_length=255, unique=True)
    phone = db.StringField(max_length=15, unique=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    verif_code = db.IntField()
    is_active = db.BooleanField(default=False)
    # TODO: implement this
    # guess_counter = db.StringField(max_length=5)

#---------------------------------------------
# model layer actions
# --------------------------------------------

def number_exists(phone_number):
    ''' checks if number exists in users db'''
    try:
        user = User.objects(phone = phone_number).get()
        if user.is_active:
            return False
    except Exception, e:
        return False
    elif:
        return True


def user_exists(user_name):
    ''' check if user name exists in users db'''
    try:
        user = User.objects(name = user_name).get()
        if user.is_active:
            return False
    except Exception, e:
        return False
    else:
        return True


def create_user(name, number):
    ''' create a new user in the db '''
    new_user = User()
    new_user.name = name
    new_user.phone = number
    new_user.save()


def delete_user(number):
    ''' deletes a user in the db given a valid number'''
    User.objects(phone = number).delete()


def set_active(number):
    ''' sets a user to active given a valid number'''
    user = User.objects(phone = number)
    user.update(set__is_active = True)


def create_message(from_name, from_phone, message_body, to_name, to_phone, guess_id):
    ''' creates a new message in the db '''
    new_message = Message()
    new_message.from_name = from_name
    new_message.from_phone = from_phone
    new_message.message_body = message_body
    new_message.to_name = to_name
    new_message.to_phone = to_phone
    new_message.guess_id = guess_id
    message.save()


def get_number_from_name(user_name):
    ''' returns a users number given their name '''
    return User.objects(name = user_name).get().phone


def get_name_from_number(number):
    ''' returns a users name given their number '''
    return User.objects(phone = number).get().name


def get_name_from_guess_id(guess_id):
    ''' returns the sender give a valid guess_id '''
    return Message.objects(guess_id = guess_id).get().from_name


def get_verif(number):
    ''' get a user's verif_code given a valid number'''
    verif = User.objects(phone = number).get().verif_code
    return verif


def set_verif(number, verif_code):
    ''' set a user's verif_code given a valid number'''
    number = "+1" + number
    user = User.objects(phone = number)
    user.update(set__verif_code = verif_code)


def get_message_list():
    ''' returns a list of all messages '''
    return list(Message.objects())


def get_user_list():
    ''' returns a list of all active users '''
    return list(User.objects(is_active = true))
