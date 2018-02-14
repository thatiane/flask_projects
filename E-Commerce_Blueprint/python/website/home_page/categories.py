# some imports
from flask import render_template
from python.database.flask_database import *

categorie = Blueprint('categorie', __name__)


# show all products in specific category

@categorie.route('/categories/<category>', methods=['post', 'get'])
def categories(category):
    cur = mysql.connection.cursor()
    cur.execute("SELECT category FROM categories")
    all_categories = cur.fetchall()
    result = cur.execute("SELECT * FROM products WHERE category=%s", [category])
    categories = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('catigories.html', categories=categories, all_categories=all_categories)
    else:
        msg = 'No Products Found!'
        return render_template('catigories.html', msg=msg, all_categories=all_categories)

