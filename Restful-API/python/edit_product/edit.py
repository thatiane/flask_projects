# some imports
from flask_mysqldb import MySQL
from cerberus import Validator
from python.token_check.check import *

edit_product_bluprint = Blueprint('edit_product_bluprint', __name__)
mysql = MySQL(app)


# product validators schema

schema = {'product_name': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'category': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'description': {'required': True, 'type': 'string', 'minlength': 10},
          'price': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'discount': {'type': 'string', 'maxlength': 10},
          'quantity': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100}}


# edit product

@edit_product_bluprint.route('/api/edit_product/<id>', methods=['PUT'])
@token_required
def edit_product(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products WHERE id = %s", [id])
    cur.close()
    if result > 0:
        v = Validator(schema)
        if request.method == 'PUT' and v.validate(request.get_json(), schema) is True:
            product_name = request.json['product_name']
            category = request.json['category']
            description = request.json['description']
            price = request.json['price']
            discount = request.json['discount']
            quantity = request.json['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, 'test', id))
                mysql.connection.commit()
                cur.close()
                return jsonify({"success": True, "message": "Edited without discount"})

            else:
                p = round((float(price) * float(discount)) / 100, 2)
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                             discount=%s, quantity=%s, files=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, 'test2', id))
                mysql.connection.commit()
                cur.close()
                return jsonify({"success": True, "message": "Edited with discount"})
    else:
        return jsonify({"success": False, "message": "product not found!"})

