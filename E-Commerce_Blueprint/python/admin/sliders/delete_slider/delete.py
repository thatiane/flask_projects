

from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *


delete_slider_admin = Blueprint('delete_slider_admin', __name__)


# admin delete slider product

@delete_slider_admin.route('/admin/delete_product_slider/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_product_slider(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name FROM slider_products WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['product_name']
    try:
        rmtree(app.root_path + r"\static\uploads\slider_products\{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM slider_products WHERE id = %s", [id])
    cur.execute("DELETE FROM slider_reviews WHERE product_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Your slider Product Has been Deleted successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))