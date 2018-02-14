# some imports
from wtforms import Form, StringField, TextAreaField, validators, IntegerField
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from shutil import rmtree
from cerberus import Validator
import os
from python.token_check.check import *

add_product_bluprint = Blueprint('add_product_bluprint', __name__)
mysql = MySQL(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# product validators schema

schema = {'product_name': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'category': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'description': {'required': True, 'type': 'string', 'minlength': 10},
          'price': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'discount': {'type': 'string', 'maxlength': 10},
          'quantity': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100}}


# add new product page

@add_product_bluprint.route('/api/add_product', methods=['post', 'get'])
@token_required
def add_product():
    v = Validator(schema)
    if request.method == 'POST':
        product_name = request.json['product_name']
        folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
        if folder == True:
            return jsonify({'message': 'Folder Already Exists', 'errors': v.errors if v.errors != {} else 'no errors'})
        cur = mysql.connection.cursor()
        cur.execute("SELECT product_name FROM products WHERE product_name = %s", [product_name])
        res = cur.fetchone()
        if product_name in str(res):
            return jsonify({'success': 'Product Already Exists', 'errors': v.errors if v.errors != {} else 'no errors'})
        print(request.get_json())
        if request.method == 'POST' and v.validate(request.get_json(), schema) is True:

        # file = request.files['file']
        # if file.filename == '':
        #     return jsonify({'success': 'False Product'})
        # if file and allowed_file(file.filename):
        #     try:
        #         rmtree(app.root_path + r"\static\uploads\products\{}".format(product_name))
        #         os.makedirs(app.root_path + r"\static\uploads\products\{}".format(product_name))
        #     except:
        #         os.makedirs(app.root_path + r"\static\uploads\products\{}".format(product_name))
        #     filename = secure_filename(file.filename)
        #     dir = app.root_path + r"\static\uploads\products\{}".format(product_name)
        #     file.save(os.path.join(dir, filename))
            category = request.json['category']
            description = request.json['description']
            price = request.json['price']
            discount = request.json['discount']
            quantity = request.json['quantity']

            if discount != '' and discount != ' ':
                p = round((float(price) * float(discount)) / 100, 2)
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                            (category, product_name, description, price, p, quantity, 'test'))
                mysql.connection.commit()
                cur.close()
                return jsonify({'success': 'True added successfully with discount'})

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                            (category, product_name, description, price, p, quantity, 'test2'))
                mysql.connection.commit()
                cur.close()
                return jsonify({'success': 'True added successfully without discount'})
    return jsonify({'success': 'general'})