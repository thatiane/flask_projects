

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_product_admin = Blueprint('delete_product_admin', __name__)

# admin delete product

@delete_product_admin.route('/admin/delete_product/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, category FROM products WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['product_name']
    category = name['category']
    try:
        rmtree(app.root_path + r"\static\uploads\products\{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM products WHERE id = %s", [id])
    cur.execute("DELETE FROM orders WHERE product_id = %s", [id])
    cur.execute("DELETE FROM reviews WHERE product_id = %s", [id])
    cur.execute("UPDATE categories SET number_of_products = number_of_products - 1 WHERE category = %s", [category])
    mysql.connection.commit()
    cur.close()
    flash('Your Product Has been Deleted successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))