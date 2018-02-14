

from flask import render_template
from python.website.login.login_check import *
from python.database.flask_database import *

account = Blueprint('account', __name__)

# user account page

@account.route('/user_account', methods=['post', 'get'])
@is_user_logged_in
def user_account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buy_orders WHERE user_name = %s", [session['user_username']])
    orders = cur.fetchall()
    cur.execute("SELECT files FROM users WHERE username = %s", [session['user_username']])
    image = cur.fetchone()
    user_image = image['files']
    return render_template('user_account.html', orders=orders, user_image=user_image)