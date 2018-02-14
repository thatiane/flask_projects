


from shutil import rmtree
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_category_admin = Blueprint('delete_category_admin', __name__)


# admin delete category

@delete_category_admin.route('/admin/delete_category/<category>', methods=['post', 'get'])
@is_admin_logged_in
def delete_category(category):
    cur = mysql.connection.cursor()
    prod = cur.execute("SELECT product_name FROM products WHERE category=%s", [category])
    if prod > 0:
        # flash('You Have products in This category', 'success')
        pass
    products = cur.fetchall()
    for product in products:
        rmtree(app.root_path + r"\static\uploads\products\{}".format(product['product_name']))
        cur.execute("DELETE FROM reviews WHERE product_name=%s", [product['product_name']])
        mysql.connection.commit()

    slider = cur.execute("SELECT product_name FROM slider_products WHERE category=%s", [category])
    if slider > 0:
        pass
    sliders = cur.fetchall()
    for slider in sliders:
        rmtree(app.root_path + r"\static\uploads\slider_products\{}".format(slider['product_name']))
        cur.execute("DELETE FROM slider_reviews WHERE product_name=%s", [slider['product_name']])
        mysql.connection.commit()

    cur.execute("DELETE FROM slider_products WHERE category=%s", [category])
    cur.execute("DELETE FROM products WHERE category=%s", [category])
    cur.execute("DELETE FROM categories Where category=%s;", [category])
    mysql.connection.commit()
    cur.close()
    flash("You Have Deleted Category With it's products Successfully!", 'success')
    return redirect(url_for('dashboard.admin_dashboard'))