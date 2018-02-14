

from python.admin.login.login_check import *
from python.database.flask_database import *

accept_order_by_user_admin = Blueprint('accept_order_by_user_admin', __name__)


# admin accept orders for user

@accept_order_by_user_admin.route('/admin/accept_order_user/<username>/<id>', methods=['post', 'get'])
@is_admin_logged_in
def accept_order_user(username, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s AND user_name = %s", (['Accepted'], id, username))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted the order Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))