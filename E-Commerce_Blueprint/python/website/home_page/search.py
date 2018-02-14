# some imports
from flask import render_template, request, redirect, url_for, flash
from python.database.flask_database import *

search = Blueprint('search', __name__)

# user search bar

@search.route('/user_search', methods=['GET', 'POST'])
def user_search():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM `buy_sell`.`products` \
                             WHERE( CONVERT(`product_name` USING utf8)\
                             LIKE %s)", [["%" + request.form['search'] + "%"]])
        categories = cur.fetchall()
        cur.close()
        if result > 0:
            return render_template('catigories.html', categories=categories)
        else:
            flash('No Products Found', 'warning')
            return redirect(url_for('web_home.home'))

