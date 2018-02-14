

from flask import request
from python.website.login.login_check import *
from python.database.flask_database import *

slider_user_review = Blueprint('slider_user_review', __name__)


# add slider product review
@slider_user_review.route('/slider_product_review/<id>', methods=['post', 'get'])
@is_user_logged_in
def slider_product_review(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT product_id FROM slider_reviews WHERE user_name = %s AND product_id = %s", [session['user_username'], id])
    if result == 0:
        cur.execute("SELECT id, product_name FROM slider_products WHERE id = %s", [id])
        product = cur.fetchone()
        product_id = product['id']
        product_name = product['product_name']
        cur.execute("SELECT id, username FROM users WHERE username = %s", [session['user_username']])
        user = cur.fetchone()
        user_id = user['id']
        user_name = user['username']

        product_rate = request.form['rate']
        review = request.form['product_review_area']

        if review == '':
            flash('You must write a review!', 'danger')
            return redirect(url_for('web_home.home'))
        else:
            cur.execute("INSERT INTO slider_reviews(user_id, user_name, product_id, product_name, rate, review)\
                         VALUES(%s, %s, %s, %s, %s, %s)", \
                        (user_id, user_name, product_id, product_name, product_rate, review))
            mysql.connection.commit()
            flash('Your review now added successfully!', 'success')
    else:
        flash('You can not add two reviews for one product!', 'danger')
    cur.close()
    return redirect(url_for('web_home.home'))