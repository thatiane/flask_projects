

from python.admin.login.login_check import *
from python.database.flask_database import *

reject_order_by_user_admin = Blueprint('reject_order_by_user_admin', __name__)


# admin reject orders for user

@reject_order_by_user_admin.route('/admin/reject_order_user/<username>/<id>', methods=['post', 'get'])
@is_admin_logged_in
def reject_order_user(username, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s AND user_name = %s", (['Rejected'], id, username))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected the order Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))
