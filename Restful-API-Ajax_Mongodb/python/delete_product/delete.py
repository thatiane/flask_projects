# some imports
from shutil import rmtree
import os
from bson.objectid import ObjectId
from python.token_check.check import *
from python.database.database import *

delete_product_bluprint = Blueprint('delete_product_bluprint', __name__)


# add new product page

@delete_product_bluprint.route('/api/delete_product/<id>', methods=['DELETE'])
# @token_required
def delete_product(id):
    if request.method == 'DELETE':
        # mongo.db.products.remove({"_id": ObjectId(id)})
        for product in mongo.db.products.find({"_id": ObjectId(id)}):
            product_name = product['product_name']
            folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
            if folder == True:
                rmtree(app.root_path + r"\static\uploads\products\{}".format(product_name))
                mongo.db.products.remove({"_id": ObjectId(id)})
                return jsonify({'success': True})
            else:
                mongo.db.products.remove({"_id": ObjectId(id)})
                return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    else:
        return jsonify({'success': False})
