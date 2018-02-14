

from python.admin.login.login_check import *
logout_admin = Blueprint('logout_admin', __name__)

# admin log out

@logout_admin.route('/admin/logout')
@is_admin_logged_in
def admin_logout():
    session.clear()
    flash('You Are Now Logged Out', 'success')
    return redirect(url_for('login_admin.admin_login'))