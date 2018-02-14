
from flask import render_template
from python.website.login.login_check import *
from python.database.flask_database import *

cart = Blueprint('cart', __name__)

# cart page

@cart.route('/add_to_cart', methods=['post', 'get'])
@is_user_logged_in
def add_to_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
    orders = cur.fetchall()
    cur.execute("SELECT user_name FROM orders WHERE user_name = %s", [session['user_username']])
    f = cur.fetchall()
    cur.execute("SELECT SUM((price * quantity) - (quantity * discount)) FROM orders WHERE user_name = %s", [session['user_username']])
    # cur.execute("SELECT SUM((price * quantity) - (quantity * discount)) AS total FROM orders WHERE user_name = %s", [session['user_username']])
    order_price = cur.fetchone()
    cur.execute("SELECT SUM(quantity) FROM orders WHERE user_name = %s", [session['user_username']])
    quantities = cur.fetchone()
    cur.close()
    return render_template('cart.html', orders=orders, price=order_price['SUM((price * quantity) - (quantity * discount))'], quantity=quantities['SUM(quantity)'], f=f)
