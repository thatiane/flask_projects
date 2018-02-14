

from python.website.login.login_check import *
from python.database.flask_database import *

delete_from_cart = Blueprint('delete_from_cart', __name__)

# delete product from cart page

@delete_from_cart.route('/delete_product_from_cart/<id>', methods=['post', 'get'])
@is_user_logged_in
def delete_product_from_cart(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE product_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('You have deleted the product successfully from your cart!', 'success')
    return redirect(url_for('cart.add_to_cart'))