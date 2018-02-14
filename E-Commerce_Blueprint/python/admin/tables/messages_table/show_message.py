

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *

show_message_admin = Blueprint('show_message_admin', __name__)

# view message page

@show_message_admin.route('/admin/message/<id>', methods=['post', 'get'])
@is_admin_logged_in
def admin_message(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contact_us WHERE id = %s ;", [id])
    current_message = cur.fetchone()
    cur.execute("UPDATE contact_us SET status = %s WHERE id = %s", (['seen'], id))
    mysql.connection.commit()

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
    return render_template('admin_message.html', admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], current_message=current_message, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)