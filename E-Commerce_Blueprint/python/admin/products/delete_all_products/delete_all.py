

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_product_admin = Blueprint('delete_all_product_admin', __name__)

# admin delete all products

@delete_all_product_admin.route('/admin/delete_all_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + r"\static\uploads\products")
        flash('You Has been Deleted All Products successfully!', 'success')
    except:
        flash('You Has been Already Deleted All Products successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))