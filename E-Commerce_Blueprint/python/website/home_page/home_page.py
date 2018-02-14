# some imports
from flask import render_template
from python.database.flask_database import *

web_home = Blueprint('web_home', __name__)

# home page

@web_home.route('/', methods=['post', 'get'])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products LIMIT 1")
    slider_products_first = cur.fetchall()
    cur.execute("SELECT * FROM slider_products LIMIT 1 OFFSET 1")
    slider_products_second = cur.fetchall()
    # cur.execute("SELECT * FROM slider_products ORDER BY id DESC LIMIT 1")
    cur.execute("SELECT * FROM slider_products LIMIT 1 OFFSET 2")
    slider_products_third = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 6;")
    latest_products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY number_of_views DESC LIMIT 3;")
    recommended_products = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY number_of_views DESC LIMIT 3 OFFSET 3")
    recommended_products_second = cur.fetchall()
    cur.close()

    return render_template('home.html', latest_products=latest_products, categories=categories, slider_products_first=slider_products_first, slider_products_second=slider_products_second, slider_products_third=slider_products_third, recommended_products=recommended_products, recommended_products_second=recommended_products_second)
