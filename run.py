import os
import urllib
import urllib2
import json
import pdb
import datetime
from wtforms import ValidationError

from app import app

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

