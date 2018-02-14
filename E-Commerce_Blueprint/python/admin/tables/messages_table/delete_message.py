

from python.admin.login.login_check import *
from python.database.flask_database import *

delete_message_admin = Blueprint('delete_message_admin', __name__)

# delete message

@delete_message_admin.route('/admin/delete_message/<id>', methods=['post', 'get'])
@is_admin_logged_in
def admin_delete_message(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_us WHERE id = %s ;", [id])
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted the message!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))