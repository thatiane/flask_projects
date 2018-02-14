

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *

orders_table_admin = Blueprint('orders_table_admin', __name__)


# admin preview all users table page

@orders_table_admin.route('/admin/orders_table')
@is_admin_logged_in
def orders_table():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT SUM(quantity) AS QUANTITY , user_name AS USERNAME, SUM((price * quantity) - (quantity * discount)) AS TOTAL FROM buy_orders T GROUP BY user_id")
    cur.execute("SELECT * FROM buy_orders ;")
    orders = cur.fetchall()

    # view messages
    cur.execute("SELECT * FROM contact_us WHERE status = %s ORDER BY id DESC LIMIT 6;", ["not_seen"])
    messages = cur.fetchall()

    # show messages number
    cur.execute("SELECT COUNT(id) FROM contact_us WHERE status = %s ", ['not_seen'])
    count_message = cur.fetchone()
    count_messages = count_message['COUNT(id)']

    # show new orders number
    cur.execute("SELECT COUNT(status) FROM buy_orders WHERE status = %s", ['Pending'])
    count_order = cur.fetchone()
    count_orders_where_pending = count_order['COUNT(status)']

    # show new orders
    cur.execute("SELECT COUNT(status), user_name FROM buy_orders WHERE status = %s GROUP BY user_name ASC LIMIT 12", ['Pending'])
    count_orders_by_user = cur.fetchall()

    cur.close()
    return render_template('admin_orders_table.html', orders=orders, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)
