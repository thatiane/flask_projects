

from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_messages_admin = Blueprint('delete_all_messages_admin', __name__)

# delete all messages

@delete_all_messages_admin.route('/admin/delete_all_messages', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_messages():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE contact_us")
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted all messages!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))