# some imports
from flask import render_template
from python.database.flask_database import *

slider = Blueprint('slider', __name__)

# preview slider product page

@slider.route('/preview_production_slider/<id>/')
def preview_production_slider(id):
    cur = mysql.connection.cursor()
    slider_reviewresult = cur.execute(
        "SELECT * FROM slider_reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    slider_review = cur.fetchone()
    cur.execute("SELECT COUNT(product_id) FROM slider_reviews WHERE product_id={}".format(id))
    reviews = cur.fetchone()
    count_reviews = reviews['COUNT(product_id)']

    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM slider_reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

    cur.execute("SELECT * FROM slider_products WHERE id={}".format(id))
    product = cur.fetchone()
    cur.execute("SELECT * FROM slider_products WHERE id != %s ORDER BY id DESC LIMIT 6", [id])
    products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("UPDATE slider_products SET number_of_views = number_of_views + 1 WHERE id={}".format(id))
    mysql.connection.commit()
    cur.close()
    return render_template('preview_production_slider.html', product=product, products=products, categories=categories,
                           slider_reviewresult=slider_reviewresult, slider_review=slider_review,
                           count_reviews=count_reviews, rate=rate)