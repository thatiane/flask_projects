
from flask import render_template, request
from python.admin.login.login_check import *
from python.database.flask_database import *

admin_search = Blueprint('admin_search', __name__)


# admin search bar

@admin_search.route('/search', methods=['GET', 'POST'])
@is_admin_logged_in
def search_admin():
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
            return redirect(url_for('dashboard.admin_dashboard'))