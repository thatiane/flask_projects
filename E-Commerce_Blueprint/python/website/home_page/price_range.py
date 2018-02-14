# some imports
from flask import render_template, request
from python.database.flask_database import *

web_home_price_range = Blueprint('web_home_price_range', __name__)


# products range price

@web_home_price_range.route('/products_price_range', methods=['post', 'get'])
def products_price_range():
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE (price BETWEEN %s AND %s)", [min_price, max_price])
    categories = cur.fetchall()
    cur.close()
    return render_template('catigories.html', categories=categories)