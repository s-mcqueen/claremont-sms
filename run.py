import os
import urllib
import urllib2
import json
import pdb
import datetime
from wtforms import ValidationError

from lib import forms, process
from app import *
from models import Message as Message
from models import User as User
from models import numberExists, userExists

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

