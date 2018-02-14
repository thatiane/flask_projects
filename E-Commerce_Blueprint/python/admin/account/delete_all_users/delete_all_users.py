

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *


delete_all_users_admin = Blueprint('delete_all_users_admin', __name__)


# admin delete all users

@delete_all_users_admin.route('/admin/delete_all_users', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_users():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT username FROM users WHERE permission = 'user'")
    if result >0:
        name = cur.fetchall()
        for n in name:
            rmtree(app.root_path + r"\static\uploads\users\{}".format(n['username']))
    elif result == 0:
        pass
    cur.execute("DELETE FROM users WHERE permission = 'user' ")
    mysql.connection.commit()
    cur.close()
    flash('You Have Deleted All Users Account with their files successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))