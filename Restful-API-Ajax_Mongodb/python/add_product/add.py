# some imports
from cerberus import Validator
import os
import datetime
from python.token_check.check import *
from python.database.database import *


add_product_bluprint = Blueprint('add_product_bluprint', __name__)

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

@add_product_bluprint.route('/api/add_product', methods=['POST', 'get'])
# @token_required
def add_product():
    v = Validator(schema)
    if request.method == 'POST':
        product_name = request.json['product_name']
        folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
        if folder == True:
            return jsonify({'message': 'Folder Already Exists', 'errors': v.errors if v.errors != {} else 'no errors'})
        for product in mongo.db.products.find({"product_name": product_name}):
            if product_name in product['product_name']:
                return jsonify({'success': 'Product Already Exists', 'errors': v.errors if v.errors != {} else 'no errors'})

        if request.method == 'POST' and v.validate(request.get_json(), schema) is True:

            category = request.json['category']
            description = request.json['description']
            price = request.json['price']
            discount = request.json['discount']
            quantity = request.json['quantity']

            if discount != '' and discount != ' ':
                p = round((float(price) * float(discount)) / 100, 2)
                pro1 = {"category": category, "product_name": product_name,
                        "description": description, "price": price,
                        "discount": p, "quantity": quantity, "files": "test",
                        "number_of_sales": 0, "number_of_views": 0,
                        "create_date": datetime.datetime.now()}
                mongo.db.products.insert(pro1)

                all1 = mongo.db.products.find({"product_name": product_name})
                al = list(all1)
                output = []
                for i in al:
                    output.append({"category": i['category'], "product_name": i['product_name'],
                                   "description": i['description'], "price": i['price'],
                                   "discount": i['discount'], "quantity": i['quantity'],
                                   "files": i['files'], "number_of_sales": i['number_of_sales'],
                                   "number_of_views": i['number_of_views'], "create_date": i['create_date'],
                                   "id": str(i['_id'])})
                return jsonify(output)


            if discount == "" or discount == " ":
                p = 0

                pro2 = {"category": category, "product_name": product_name,
                        "description": description, "price": price,
                        "discount": p, "quantity": quantity, "files": "test2",
                        "number_of_sales": 0, "number_of_views": 0,
                        "create_date": datetime.datetime.now()}
                mongo.db.products.insert(pro2)

                all2 = mongo.db.products.find({"product_name": product_name})
                al = list(all2)
                output = []
                for i in al:
                    output.append({"category": i['category'], "product_name": i['product_name'],
                                   "description": i['description'], "price": i['price'],
                                   "discount": i['discount'], "quantity": i['quantity'],
                                   "files": i['files'], "number_of_sales": i['number_of_sales'],
                                   "number_of_views": i['number_of_views'], "create_date": i['create_date'],
                                   "id": str(i['_id'])})
                return jsonify(output)
    return jsonify({'success': 'general'})