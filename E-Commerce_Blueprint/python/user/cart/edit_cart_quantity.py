
from flask import request
from python.website.login.login_check import *
from python.database.flask_database import *

edit_quantity = Blueprint('edit_quantity', __name__)

# edit cart product quantity in cart page

@edit_quantity.route('/edit_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def edit_cart_product_quantity(id):
    quantity = request.form['quantity']
    if int(quantity) >= 1:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET quantity = %s WHERE product_id = %s", [quantity, id])
        mysql.connection.commit()
        cur.close()
        flash('You have updated the product quantity successfully!', 'success')
    else:
        pass
        flash('You can not put the quantity less than one!', 'danger')
    return redirect(url_for('cart.add_to_cart'))