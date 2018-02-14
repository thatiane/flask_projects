
from shutil import rmtree
from python.website.login.login_check import *
from python.database.flask_database import *

delete_account = Blueprint('delete_account', __name__)

# delete user account

@delete_account.route('/delete_user_account', methods=['post', 'get'])
@is_user_logged_in
def delete_user_account():
    rmtree(app.root_path + r"\static\uploads\users\{}".format(session['user_username']))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM buy_orders WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM reviews WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM slider_reviews WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM users WHERE username = %s", [session['user_username']])
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('You Have Deleted Your Account successfully!', 'success')
    return redirect(url_for('web_home.home'))