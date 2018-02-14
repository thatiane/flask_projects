

from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_not_seen_messages_admin = Blueprint('delete_all_not_seen_messages_admin', __name__)

# delete all not seen messages

@delete_all_not_seen_messages_admin.route('/admin/delete_all_not_seen_messages', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_not_seen_messages():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_us WHERE status = %s ", ['not_seen'])
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted all not seen messages!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))