

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


edit_product_admin = Blueprint('edit_product_admin', __name__)


# admin edit product page

@edit_product_admin.route('/admin/edit_product/<id>', methods=['post', 'get'])
@is_admin_logged_in
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id={}".format(id))
    product = cur.fetchone()

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
    form = AddProductForm(request.form)
    form.product_name.data = product['product_name']
    form.description.data = product['description']
    form.price.data = product['price']
    form.quantity.data = product['quantity']
    # form.discount.data = product['discount']


    d = round((float(product['discount']) * float(100)) / float(form.price.data), 2)
    form.discount.data = d

    if request.method == 'POST' and form.validate():
        product_name = request.form['product_name']

        folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
        if folder == True and form.product_name.data == product_name:
            pass
        elif folder == False and form.product_name.data != product_name:
            pass
        else:
            flash('Folder Name Already Exists', 'warning')
            return redirect(request.url)

        file = request.files['file']
        if file and allowed_file(file.filename):
            rmtree(app.root_path + r"\static\uploads\products\{}".format(product['product_name']))
            os.makedirs(app.root_path + r"\static\uploads\products\{}".format(product_name))
            filename = secure_filename(file.filename)
            dir = app.root_path + r"\static\uploads\products\{}".format(product_name)
            file.save(os.path.join(dir, filename))

            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, filename, id))
                mysql.connection.commit()
                cur.close()
                flash('Your Product Has been Edited successfully!', 'success')
                return redirect(url_for('dashboard.admin_dashboard'))

            p = round((float(price) * float(discount)) / 100, 2)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, filename, id))
            mysql.connection.commit()
            cur.close()
            flash('Your Product Has been Edited successfully!', 'success')
            return redirect(url_for('dashboard.admin_dashboard'))
        elif file.filename == '' or 'file' not in request.files:
            os.rename(os.path.join(app.root_path + r"\static\uploads\products\{}".format(product['product_name'])),
                      os.path.join(app.root_path + r"\static\uploads\products\{}".format(product_name)))
            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                             discount=%s, quantity=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, id))
                mysql.connection.commit()
                cur.close()
                flash('Your Product Has been Edited successfully!', 'success')
                return redirect(url_for('dashboard.admin_dashboard'))

            p = round((float(price) * float(discount)) / 100, 2)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, id))
            mysql.connection.commit()
            cur.close()
            flash('Your Product Has been Edited successfully!', 'success')
            return redirect(url_for('dashboard.admin_dashboard'))
    return render_template('admin_edit_production.html', form=form, categories=categories,
                           admin_name=session['admin_username'], admin_image=session['admin_image'],
                           permission=session['permission'], messages=messages, count_messages=count_messages,
                           count_orders_where_pending=count_orders_where_pending,
                           count_orders_by_user=count_orders_by_user)