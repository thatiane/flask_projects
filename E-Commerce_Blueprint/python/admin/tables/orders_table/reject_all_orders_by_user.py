

from python.admin.login.login_check import *
from python.database.flask_database import *

reject_all_orders_by_user_admin = Blueprint('reject_all_orders_by_user_admin', __name__)

# admin reject all orders for user

@reject_all_orders_by_user_admin.route('/admin/reject_all_orders_user/<username>', methods=['post', 'get'])
@is_admin_logged_in
def reject_all_orders_user(username):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE user_name = %s", (['Rejected'], username))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected all orders Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))
