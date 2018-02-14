# some imports
from flask import render_template
from python.database.flask_database import *

all_products = Blueprint('all_products', __name__)

# all products page

@all_products.route('/products/<id>')
def products(id):
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM products ORDER BY id DESC;")
    # all_products = cur.fetchall()

    cur.execute("SELECT COUNT(id) FROM products ORDER BY id ASC;")
    pr = cur.fetchone()
    number_of_products = int(pr['COUNT(id)'] / 10)

    off = (int(id) * 10) - 10
    cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 10 OFFSET %s;", [off])
    all_products = cur.fetchall()


    # for product in all_products:
    #     product_name = product['product_name']
    #     print(product_name)
    #     cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_name = %s;", [product_name])
    #     rate = cur.fetchall()
    #     print(rate)
    cur.close()
    return render_template('all_products.html', all_products=all_products, number_of_products=number_of_products)
