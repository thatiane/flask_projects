

from python.website.login.login_check import *
from python.database.flask_database import *

increase_quantity = Blueprint('increase_quantity', __name__)


# increase cart product quantity in cart page

@increase_quantity.route('/increase_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def increase_cart_product_quantity(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET quantity = quantity + 1 WHERE product_id = {}".format(id))
    mysql.connection.commit()
    cur.close()
    flash('You have updated the product quantity successfully!', 'success')
    return redirect(url_for('cart.add_to_cart'))