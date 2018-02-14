# some imports
from flask_mysqldb import MySQL
from flask import render_template
from python.token_check.check import *

all_productss = Blueprint('all_productss', __name__)
mysql = MySQL(app)



# all products page

@all_productss.route('/api/all_products', methods=['GET'])
# @token_required
def all_products():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products")
    cur.close()
    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products ORDER BY id DESC;")
        all_products = cur.fetchall()
        cur.close()
        return jsonify(all_products)
    else:
        return jsonify({'message': 'no data found'})
