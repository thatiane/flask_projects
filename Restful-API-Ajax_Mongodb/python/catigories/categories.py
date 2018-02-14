# some imports
from flask_mysqldb import MySQL
from python.token_check.check import *

category = Blueprint('category', __name__)
mysql = MySQL(app)



# all products by category page

@category.route('/api/categories/<categoryy>', methods=['post'])
@token_required
def categories(categoryy):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products WHERE category = %s", [categoryy])
    cur.close()
    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE category = %s ORDER BY id DESC;", [categoryy])
        all_products = cur.fetchall()
        cur.close()
        return jsonify({'all_products_data': all_products})
    else:
        return jsonify({'message': 'no data found'})
