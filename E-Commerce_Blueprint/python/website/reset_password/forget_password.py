# some imports
from flask import render_template
from python.database.flask_database import *

forget_password = Blueprint('forget_password', __name__)

# user reset password page

@forget_password.route('/user_forget_password')
def user_forget_password():
    return render_template('user_forget_password.html')
