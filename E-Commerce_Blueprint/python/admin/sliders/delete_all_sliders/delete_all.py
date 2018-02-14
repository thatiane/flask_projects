

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_slider_admin = Blueprint('delete_all_slider_admin', __name__)


# admin delete all slider products

@delete_all_slider_admin.route('/admin/delete_all_slider_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_slider_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + r"\static\uploads\slider_products")
        flash('You Has been Deleted All slider Products successfully!', 'success')
    except:
        flash('You Has been Already Deleted All slider Products successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))