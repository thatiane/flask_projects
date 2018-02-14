
from flask import redirect, url_for, session, flash, Blueprint
from functools import wraps

check = Blueprint('check', __name__)

# check if user is still logged in

def is_user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login.user_login'))
    return wrap