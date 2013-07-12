import datetime
from app import db

class Message(db.DynamicDocument):
    ''' class to hold the message fields'''
    from_name = db.StringField(max_length=255)
    from_phone = db.StringField(max_length=15)
    
    # message or message_body???
    message_body = db.StringField(max_length=400)
    to_name = db.StringField(max_length=255)
    to_phone = db.StringField(max_length=15)
    created_at = db.DateTimeField(default=datetime.utcnow())
    guess_id = db.StringField(max_length=5) 


class User(db.DynamicDocument):
    ''' class to hold the user fields'''
    name = db.StringField(max_length=255, unique=True)
    phone = db.StringField(max_length=15, unique=True)
    created_at = db.DateTimeField(default=datetime.utcnow())
    verif_code = db.IntField()
    is_active = db.BooleanField(default=False)
    # guess_counter = db.StringField(max_length=5)


def numberExists(phone_number):
    ''' checks if number exists in users db'''

    try:
        user = User.objects(phone = phone_number).get()
    except Exception, e:
        return False
    else:
        return True


def userExists(user_name):
    ''' check if user name exists in users db'''

    try:
        user = User.objects(name = user_name).get()
    except Exception, e:
        return False
    else:
        return True


def createUser(name, phone):
    ''' create a new user in the db '''
    new_user = User()
    new_user.name = name
    new_user.phone = phone
    new_user.save()


def deleteUser(number):
    User.objects(phone = number).delete()


def setActive(number):
    number = "+1" + number
    user = User.objects(phone = number)
    user.update(set__is_active = True)


def createMessage(from_name, from_phone, message_body, to_name, to_phone, guess_id):
    ''' create a new message in the db '''
    new_message = Message()
    new_message.from_name = from_name
    new_message.from_phone = from_phone
    new_message.message_body = message_body
    new_message.to_name = to_name
    new_message.to_phone = to_phone
    new_message.guess_id = guess_id
    message.save()
