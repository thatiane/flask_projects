# some imports
from flask_mysqldb import MySQL
from python.token_check.check import *

one_product = Blueprint('one_product', __name__)
mysql = MySQL(app)


# product page

@one_product.route('/api/product/<id>', methods=['post'])
@token_required
def product(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products WHERE id = %s;", [id])
    cur.close()
    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE id = %s;", [id])
        product = cur.fetchall()
        cur.close()
        return jsonify({'product_data': product})
    else:
        return jsonify({'message': 'no data found for this product'})

