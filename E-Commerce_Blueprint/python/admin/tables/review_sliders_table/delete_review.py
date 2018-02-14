

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_slider_review_admin = Blueprint('delete_slider_review_admin', __name__)

# admin delete slider product review

@delete_slider_review_admin.route('/admin/delete_review_slider_product/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_review_slider_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM slider_reviews WHERE product_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Slider product review has been deleted successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))