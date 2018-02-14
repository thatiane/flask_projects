

from flask import render_template, request
from wtforms import Form, StringField, TextAreaField, validators, IntegerField
from python.website.login.login_check import *
from python.database.flask_database import *

user_buy = Blueprint('user_buy', __name__)

# user registration validators form

class CartbuyForm(Form):
    address = StringField('Address', [validators.InputRequired(), validators.length(min=10, max=200)])
    phone_number = IntegerField('Phone Number', [validators.InputRequired()])
    comments = TextAreaField('Comments', [validators.InputRequired()])

# buy orders page

@user_buy.route('/buy', methods=['post', 'get'])
@is_user_logged_in
# buy orders page

@app.route('/buy', methods=['post', 'get'])
@is_user_logged_in
def buy():
    cur = mysql.connection.cursor()
    nat = cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
    if nat > 0:
        cur.close()
        form = CartbuyForm(request.form)
        if request.method == 'POST' and form.validate():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
            buy_orders = cur.fetchall()
            for order in buy_orders:
                user_id = order['user_id']
                user_name = order['user_name']
                product_id = order['product_id']
                product_name = order['product_name']
                quantity = order['quantity']
                price = order['price']
                discount = order['discount']
                files = order['files']
                cur.execute("INSERT INTO buy_orders(user_id, user_name, status, product_id, product_name,\
                                                                quantity, price, discount, files)\
                                                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (user_id, user_name, 'Pending', product_id, product_name, \
                             quantity, price, discount, files))
                mysql.connection.commit()
            result = cur.execute("SELECT country FROM buy_orders WHERE country = '' AND user_name = %s", [session['user_username']])
            if result > 0:
                country = request.form['country']
                region = request.form['region']
                address = form.address.data
                phone_number = form.phone_number.data
                comments = form.comments.data
                cur.execute("UPDATE buy_orders SET country = %s, region = %s, address = %s, phone_number = %s, comments = %s WHERE  country = '' AND user_name = %s", \
                    [country, region, address, phone_number, comments, session['user_username']])

                cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
                confirm_orders = cur.fetchall()
                for confirm_order in confirm_orders:
                    product_name = confirm_order['product_name']
                    quantity = confirm_order['quantity']
                    cur.execute("UPDATE products SET number_of_sales = number_of_sales + 1 WHERE product_name = %s", [product_name])
                    cur.execute("UPDATE products SET quantity = quantity - %s WHERE product_name = %s", [quantity, product_name])
                    mysql.connection.commit()

                for confir_order in confirm_orders:
                    produc_name = confir_order['product_name']
                    quantity = confir_order['quantity']
                    cur.execute("UPDATE slider_products SET number_of_sales = number_of_sales + 1 WHERE product_name = %s", [produc_name])
                    cur.execute("UPDATE slider_products SET quantity = quantity - %s WHERE product_name = %s", [quantity, produc_name])
                    mysql.connection.commit()

                cur.execute("DELETE FROM orders WHERE user_name = %s", [session['user_username']])
                mysql.connection.commit()
                cur.close()
                flash('Your order is successfully sent!', 'success')
                return redirect(url_for('web_home.home'))
            elif result == 0:
                cur.close()
                flash('you can not be able to buy until you add product to your cart', 'danger')
                return redirect(url_for('cart.add_to_cart'))
        return render_template('buy.html', form=form)
    elif nat == 0:
        cur.close()
        flash('you can not be able to buy until you add product to your cart', 'danger')
        return redirect(url_for('cart.add_to_cart'))