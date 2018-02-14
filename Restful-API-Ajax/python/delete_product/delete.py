# some imports
from flask_mysqldb import MySQL
from shutil import rmtree
import os
from python.token_check.check import *

delete_product_bluprint = Blueprint('delete_product_bluprint', __name__)
mysql = MySQL(app)


# add new product page

@delete_product_bluprint.route('/api/delete_product/<id>', methods=['DELETE'])
# @token_required
def delete_product(id):
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM products WHERE id = %s", [id])
        res = cur.fetchone()
        product_name = res['product_name']
        cur.close()
        if result > 0:
            folder = os.path.exists(app.root_path + r"\static\uploads\products\{}".format(product_name))
            if folder == True:
                    rmtree(app.root_path + r"\static\uploads\products\{}".format(product_name))
                    cur = mysql.connection.cursor()
                    cur.execute("DELETE FROM products WHERE product_name = %s", [product_name])
                    mysql.connection.commit()
                    cur.close()
                    return jsonify({'success': True})
            else:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM products WHERE product_name = %s", [product_name])
                mysql.connection.commit()
                cur.close()
                return jsonify({'success': True})
        else:
            return jsonify({'success': False, "message": "product has been deleted already!"})
    else:
        return jsonify({'success': False})
