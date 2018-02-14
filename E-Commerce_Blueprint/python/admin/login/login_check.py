
from flask import redirect, url_for, session, flash, Blueprint
from functools import wraps

check_admin = Blueprint('check_admin', __name__)


# check if admin is still logged in

def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session :
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login_admin.admin_login'))
    return wrap