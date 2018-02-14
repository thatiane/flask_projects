

from python.admin.login.login_check import *
from python.database.flask_database import *

accept_all_order_by_user_admin = Blueprint('accept_all_order_by_user_admin', __name__)

# admin accept all orders for user

@accept_all_order_by_user_admin.route('/admin/accept_all_orders_user/<username>', methods=['post', 'get'])
@is_admin_logged_in
def accept_all_orders_user(username):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE user_name = %s ", (['Accepted'], username))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted all orders Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))