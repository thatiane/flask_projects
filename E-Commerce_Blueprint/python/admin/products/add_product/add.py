

from flask import render_template, request
from werkzeug.utils import secure_filename
from shutil import rmtree
from wtforms import Form, StringField, TextAreaField, validators, IntegerField
from python.admin.login.login_check import *
from python.database.flask_database import *
import os


# product validators form

class AddProductForm(Form):
    product_name = StringField('Name Of Product', [validators.InputRequired(), validators.length(min=1, max=180)])
    description = TextAreaField('Description', [validators.InputRequired()])
    price = IntegerField('Price', [validators.InputRequired()])
    discount = StringField('Discount Percentage %')
    quantity = StringField('Quantity', [validators.InputRequired()])
    # files = FileField('Add picture to Your Product', [validators.InputRequired()])


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


add_product_admin = Blueprint('add_product_admin', __name__)

# admin add new product page

@add_product_admin.route('/admin/add_product', methods=['post', 'get'])
@is_admin_logged_in
def admin_add_product():
    form = AddProductForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()

    # view messages
    cur.execute("SELECT * FROM contact_us WHERE status = %s ORDER BY id DESC LIMIT 6;", ["not_seen"])
    messages = cur.fetchall()

    # show messages number
    cur.execute("SELECT COUNT(id) FROM contact_us WHERE status = %s ", ['not_seen'])
    count_message = cur.fetchone()
    count_messages = count_message['COUNT(id)']

    # show new orders number
    cur.execute("SELECT COUNT(status) FROM buy_orders WHERE status = %s", ['Pending'])
    count_order = cur.fetchone()
    count_orders_where_pending = count_order['COUNT(status)']

    # show new orders
    cur.execute("SELECT COUNT(status), user_name FROM buy_orders WHERE status = %s GROUP BY user_name ASC LIMIT 12",
                ['Pending'])
    count_orders_by_user = cur.fetchall()

    cur.close()
    if result > 0:
        if request.method == 'POST' and form.validate():
            product_name = form.product_name.data

            folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
            if folder == True:
                flash('Folder Name Already Exists', 'warning')
                return redirect(url_for('add_product_admin.admin_add_product'))
            cur = mysql.connection.cursor()
            cur.execute("SELECT product_name FROM products WHERE product_name = %s", [product_name])
            res = cur.fetchone()
            if product_name in str(res):
                msg = "Product Name Already Exists"
                return render_template('admin_add_production.html', form=form, msg=msg,
                                       admin_name=session['admin_username'], admin_image=session['admin_image'])

            if request.method == 'POST' and form.validate():
                file = request.files['file']
                if file.filename == '':
                    flash('You Have to Select a File!', 'warning')
                if file and allowed_file(file.filename):
                    try:
                        rmtree(app.root_path + r"\static\uploads\products\{}".format(product_name))
                        os.makedirs(app.root_path + r"\static\uploads\products\{}".format(product_name))
                    except:
                        os.makedirs(app.root_path + r"\static\uploads\products\{}".format(product_name))
                    filename = secure_filename(file.filename)
                    dir = app.root_path + r"\static\uploads\products\{}".format(product_name)
                    file.save(os.path.join(dir, filename))
                    category = request.form['categories']
                    description = form.description.data.lower()
                    price = form.price.data
                    discount = form.discount.data
                    quantity = form.quantity.data

                    if discount != '' and discount != ' ':
                        p = round((float(price) * float(discount)) / 100, 2)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        cur.execute(
                            "UPDATE categories SET number_of_products = number_of_products + 1 WHERE category = %s",
                            [category])
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published successfully!', 'success')
                        return redirect(url_for('dashboard.admin_dashboard'))

                    if discount == "" or discount == " ":
                        p = 0
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        cur.execute(
                            "UPDATE categories SET number_of_products = number_of_products + 1 WHERE category = %s",
                            [category])
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published successfully!', 'success')
                        return redirect(url_for('dashboard.admin_dashboard'))

    elif result == 0:
        cur.close()
        flash('Create an category first to add a new product', 'warning')
        return redirect(url_for('dashboard.admin_dashboard'))

    return render_template('admin_add_production.html', form=form, categories=categories,
                           admin_name=session['admin_username'], admin_image=session['admin_image'],
                           permission=session['permission'], messages=messages, count_messages=count_messages,
                           count_orders_where_pending=count_orders_where_pending,
                           count_orders_by_user=count_orders_by_user)

    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO products(category, product_name, description, price, discount, files)\
    #              VALUES(%s, %s, %s, %s, %s, %s)", \
    #             (category, product_name, description, price, p, filename))
    # mysql.connection.commit()
    # cur.close()
    # flash('Your Product is published successfully!', 'success')
    # return redirect(url_for('admin_dashboard'))
    # return render_template('admin_add_production.html', form=form, categories=categories)