# some imports
from python.token_check.check import *
from python.database.database import *

all_productss = Blueprint('all_productss', __name__)


# all products page

@all_productss.route('/api/all_products', methods=['GET'])
# @token_required
def all_products():
    all = mongo.db.products.find().sort('create_date', pymongo.DESCENDING)
    if all:
        al = list(mongo.db.products.find().sort('create_date', pymongo.DESCENDING))
        output = []
        for i in al:
            output.append({"category": i['category'], "product_name": i['product_name'],
                           "description": i['description'], "price": i['price'],
                           "discount": i['discount'], "quantity": i['quantity'],
                           "files": i['files'], "number_of_sales": i['number_of_sales'],
                           "number_of_views": i['number_of_views'], "create_date": i['create_date'],
                           "id": str(i['_id'])})
        return jsonify(output)
    else:
        return jsonify({'message': 'no data found'})
