

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *


admin_show_product = Blueprint('admin_show_product', __name__)

# admin preview product

@admin_show_product.route('/admin/product/<id>')
@is_admin_logged_in
def show_product_admin(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", [id])
    product = cur.fetchone()
    reviewresult = cur.execute("SELECT * FROM reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    review = cur.fetchone()
    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

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
    return render_template('admin_product.html', product=product, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], reviewresult=reviewresult, review=review, rate=rate, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)