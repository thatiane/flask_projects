

from python.admin.login.login_check import *
from python.database.flask_database import *

reject_order_admin = Blueprint('reject_order_admin', __name__)

# admin reject orders

@reject_order_admin.route('/admin/reject_orders/<id>', methods=['post', 'get'])
@is_admin_logged_in
def reject_orders(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s", (['Rejected'], id))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected the order Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))