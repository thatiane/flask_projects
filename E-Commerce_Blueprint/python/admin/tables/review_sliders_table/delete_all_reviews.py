

from python.admin.login.login_check import *
from python.database.flask_database import *

admin_delete_all_slider_reviews = Blueprint('admin_delete_all_slider_reviews', __name__)
# admin delete all products reviews

@admin_delete_all_slider_reviews.route('/admin/delete_all_slider_products_reviews', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_slider_reviews_admin():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    flash('All slider products reviews has been deleted successfully!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))