


from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_categories_admin = Blueprint('delete_all_categories_admin', __name__)


# admin delete all categories

@delete_all_categories_admin.route('/admin/delete_all_categories', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_categories():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE categories")
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE orders")
    cur.execute("TRUNCATE buy_orders")
    cur.execute("TRUNCATE reviews")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + r"\static\uploads\products")
        rmtree(app.root_path + r"\static\uploads\slider_products")
        flash('You Has been Deleted All Categories and Products Successfully!', 'success')
    except:
        flash('You Has been Deleted All Categories and Products Successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))