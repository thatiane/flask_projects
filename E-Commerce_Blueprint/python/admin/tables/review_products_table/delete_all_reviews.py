

from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *

delete_all_reviews_admin = Blueprint('delete_all_reviews_admin', __name__)

# admin delete all products reviews

@delete_all_reviews_admin.route('/admin/delete_all_review_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_review_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE reviews")
    mysql.connection.commit()
    cur.close()
    flash('All products reviews has been deleted successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))
