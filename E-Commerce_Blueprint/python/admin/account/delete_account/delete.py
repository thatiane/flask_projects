


from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_user_admin = Blueprint('delete_user_admin', __name__)


# admin delete user

@delete_user_admin.route('/admin/delete_user/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['username']
    try:
        rmtree(app.root_path + r"\static\uploads\users\{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM orders WHERE user_name = %s", [n])
    cur.execute("DELETE FROM buy_orders WHERE user_name = %s", [n])
    cur.execute("DELETE FROM reviews WHERE user_name = %s", [n])
    cur.execute("DELETE FROM slider_reviews WHERE user_name = %s", [n])
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('You Have Deleted User Account successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))