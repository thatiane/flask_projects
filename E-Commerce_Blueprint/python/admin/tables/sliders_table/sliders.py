

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *


sliders_table_admin = Blueprint('sliders_table_admin', __name__)


# admin preview all slider products table page

@sliders_table_admin.route('/admin/slider_products_table')
@is_admin_logged_in
def slider_products_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products")
    slider_products = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM slider_products")
    sliders = cur.fetchone()
    count_sliders = sliders['COUNT(id)']

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
    return render_template('admin_slider_products_table .html', slider_products=slider_products, count_sliders=count_sliders, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)