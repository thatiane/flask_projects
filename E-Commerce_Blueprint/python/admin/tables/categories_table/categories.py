

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *


categories_table_admin = Blueprint('categories_table_admin', __name__)


# admin preview all categories table page

@categories_table_admin.route('/admin/categories_table')
@is_admin_logged_in
def categories_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    cur.execute("SELECT COUNT(category) FROM categories")
    category = cur.fetchone()
    count_categories = category['COUNT(category)']
    cur.execute("SELECT COUNT(id) FROM products")
    products = cur.fetchone()
    count_products = products['COUNT(id)']

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
    return render_template('admin_categories_table.html', categories=categories, count_products=count_products, count_categories=count_categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)