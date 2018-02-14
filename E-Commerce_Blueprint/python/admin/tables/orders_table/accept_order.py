

from python.admin.login.login_check import *
from python.database.flask_database import *

accept_order_admin = Blueprint('accept_order_admin', __name__)

# admin accept orders

@accept_order_admin.route('/admin/accept_orders/<id>', methods=['post', 'get'])
@is_admin_logged_in
def accept_orders(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s", (['Accepted'], id))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted the order Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))