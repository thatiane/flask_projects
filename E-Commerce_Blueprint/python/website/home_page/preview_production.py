# some imports
from flask import render_template
from python.database.flask_database import *

product = Blueprint('product', __name__)

# preview product page

@product.route('/preview_production/<id>/')
def preview_production(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(product_id) FROM reviews WHERE product_id={}".format(id))
    reviews = cur.fetchone()
    count_reviews = reviews['COUNT(product_id)']

    reviewresult = cur.execute("SELECT * FROM reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    review = cur.fetchone()

    cur.execute("SELECT * FROM products WHERE id={}".format(id))
    product = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE id != %s ORDER BY id DESC LIMIT 6", [id])
    products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("UPDATE products SET number_of_views = number_of_views + 1 WHERE id={}".format(id))
    mysql.connection.commit()

    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

    cur.close()
    return render_template('preview_production.html', product=product, products=products, categories=categories,
                           count_reviews=count_reviews, review=review, reviewresult=reviewresult, rate=rate)
