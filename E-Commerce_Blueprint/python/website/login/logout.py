
from python.website.login.login_check import *

logout = Blueprint('logout', __name__)

# user log out

@logout.route('/user_logout')
@is_user_logged_in
def user_logout():
    session.clear()
    flash('You Are Now Logged Out', 'success')
    return redirect(url_for('login.user_login'))