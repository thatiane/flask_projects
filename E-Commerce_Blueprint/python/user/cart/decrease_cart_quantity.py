

from python.website.login.login_check import *
from python.database.flask_database import *

decrease_quantity = Blueprint('decrease_quantity', __name__)


# decrease cart product quantity in cart page

@decrease_quantity.route('/decrease_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def decrease_cart_product_quantity(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT quantity FROM orders WHERE product_id = %s", [id])
    cart_product = cur.fetchone()
    product_quantity = cart_product['quantity']
    if product_quantity <= 1:
        flash('You can not put the quantity less than one!', 'danger')
        pass
    if product_quantity > 1:
        cur.execute("UPDATE orders SET quantity = quantity - 1 WHERE product_id = {}".format(id))
        mysql.connection.commit()
        flash('You have updated the product quantity successfully!', 'success')
    cur.close()
    return redirect(url_for('cart.add_to_cart'))