# some imports
from cerberus import Validator
from bson.objectid import ObjectId
import datetime

from python.token_check.check import *
from python.database.database import *

edit_product_bluprint = Blueprint('edit_product_bluprint', __name__)


# product validators schema

schema = {'product_name': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'category': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 255},
          'description': {'required': True, 'type': 'string', 'minlength': 10},
          'price': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'discount': {'type': 'string', 'maxlength': 10},
          'quantity': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100}}


# edit product

@edit_product_bluprint.route('/api/edit_product/<id>', methods=['PUT'])
# @token_required
def edit_product(id):
    result = mongo.db.products.find_one({"_id": ObjectId(id)})
    if result:
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
                mongo.db.products.update({"_id": ObjectId(id)},
                                         {"$set": {"category": category,
                                                   "product_name": product_name,
                                                   "description": description, "price": price,
                                                   "discount": p, "quantity": quantity,
                                                   "files": "test"}})
                return jsonify({"message": "Product updated!"})

            else:
                p = round((float(price) * float(discount)) / 100, 2)
                mongo.db.products.update({"_id": ObjectId(id)},
                                             {"$set": {"category": category,
                                                       "product_name": product_name,
                                                       "description": description, "price": price,
                                                       "discount": p, "quantity": quantity,
                                                       "files": "test2"}})
                return jsonify({"message": "Product updated"})
        else:
            return jsonify({"success": False, "message": "product not found!"})
    else:
        return jsonify({"success": False, "message": "product not found!"})

