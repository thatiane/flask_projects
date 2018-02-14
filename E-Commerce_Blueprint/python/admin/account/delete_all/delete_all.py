

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *


delete_all_admin = Blueprint('delete_all_admin', __name__)

# admin delete all accounts

@delete_all_admin.route('/admin/delete_all_accounts', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_accounts():
    try:
        rmtree(app.root_path + r"\static\uploads\users")
        rmtree(app.root_path + r"\static\uploads\products")
        rmtree(app.root_path + r"\static\uploads\slider_products")
    except:
        pass
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE users")
    cur.execute("TRUNCATE categories")
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE orders")
    cur.execute("TRUNCATE buy_orders")
    cur.execute("TRUNCATE reviews")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('You Have Deleted All Accounts with their files successfully!', 'success')
    return redirect(url_for('admin_login'))