
from flask import render_template
from python.admin.login.login_check import *
from python.database.flask_database import *
dashboard = Blueprint('dashboard', __name__)


# admin dashboard page

@dashboard.route('/admin/', methods=['post', 'get'])
@is_admin_logged_in
def admin_dashboard():
    cur = mysql.connection.cursor()

    # check if admin changed his profile picture
    cur.execute("SELECT files, permission FROM users WHERE username = %s", [session['admin_username']])
    files = cur.fetchone()
    image = files['files']
    session['admin_image'] = image

    # count slider products
    cur.execute("SELECT COUNT(id) FROM slider_products")
    sliders = cur.fetchone()
    count_sliders = sliders['COUNT(id)']
    # count products
    cur.execute("SELECT COUNT(id) FROM products")
    products = cur.fetchone()
    count_products = products['COUNT(id)']

    # count users
    cur.execute("SELECT COUNT(id) FROM users")
    users = cur.fetchone()
    count_users = users['COUNT(id)']
    # count categories
    cur.execute("SELECT COUNT(category) FROM categories")
    categories = cur.fetchone()
    count_categories = categories['COUNT(category)']

    # count number of sales for products
    cur.execute("SELECT SUM(number_of_sales) FROM products")
    number_of_sales = cur.fetchone()
    count_number_of_sales = number_of_sales['SUM(number_of_sales)']
    # count number of sales for slider products
    cur.execute("SELECT SUM(number_of_sales) FROM slider_products")
    number_of_sales = cur.fetchone()
    count_number_of_sales_slider = number_of_sales['SUM(number_of_sales)']

    # show product where it has a big number of sales
    cur.execute("SELECT * FROM products ORDER BY number_of_sales DESC LIMIT 1")
    product_saled = cur.fetchone()
    # show product where it has a small number of sales
    cur.execute("SELECT * FROM products ORDER BY number_of_sales ASC LIMIT 1")
    product_saled_low = cur.fetchone()

    # show slider product where it has a big number of sales
    cur.execute("SELECT * FROM slider_products ORDER BY number_of_sales DESC LIMIT 1")
    slider_saled = cur.fetchone()
    # show slider product where it has a small number of sales
    cur.execute("SELECT * FROM slider_products ORDER BY number_of_sales ASC LIMIT 1")
    slider_saled_low = cur.fetchone()

    # show slider product where it has a big number of rates
    cur.execute("SELECT * FROM slider_reviews ORDER BY rate DESC LIMIT 1")
    slider_big = cur.fetchone()
    # show slider product where it has a small number of rates
    cur.execute("SELECT * FROM slider_reviews ORDER BY rate ASC LIMIT 1")
    slider_small = cur.fetchone()

    # show product where it has a big number of rates
    cur.execute("SELECT * FROM reviews ORDER BY rate DESC LIMIT 1")
    product_big = cur.fetchone()
    # show product where it has a small number of rates
    cur.execute("SELECT * FROM reviews ORDER BY rate ASC LIMIT 1")
    product_small = cur.fetchone()

    # show product number of sales in last week
    cur.execute("SELECT SUM(number_of_sales) FROM products WHERE create_date >= current_date - 7")
    product_week = cur.fetchone()
    product_last_week = product_week['SUM(number_of_sales)']
    # show slider product number of sales in last week
    cur.execute("SELECT SUM(number_of_sales) FROM slider_products WHERE create_date >= current_date - 7")
    slider_week = cur.fetchone()
    slider_last_week = slider_week['SUM(number_of_sales)']

    # show product number in last week
    cur.execute("SELECT COUNT(product_name) FROM products WHERE create_date >= current_date - 7")
    product_add_week = cur.fetchone()
    product_add = product_add_week['COUNT(product_name)']
    # show slider product number in last week
    cur.execute("SELECT COUNT(product_name) FROM slider_products WHERE create_date >= current_date - 7")
    slider_add_week = cur.fetchone()
    slider_add = slider_add_week['COUNT(product_name)']

    # show total avg rate from all reviews
    cur.execute(
        "SELECT SUM(rate) / COUNT(rate) AS AVG_RATE FROM (SELECT rate FROM slider_reviews UNION ALL SELECT rate FROM reviews) T;")
    avg_rate = cur.fetchone()
    total_avg_rate = avg_rate['AVG_RATE']

    # view messages
    cur.execute("SELECT * FROM contact_us WHERE status = %s ORDER BY id DESC LIMIT 6;", ["not_seen"])
    messages = cur.fetchall()

    # show messages number
    cur.execute("SELECT COUNT(id) FROM contact_us WHERE status = %s ", ['not_seen'])
    count_message = cur.fetchone()
    count_messages = count_message['COUNT(id)']

    # show new orders number
    cur.execute("SELECT COUNT(status) FROM buy_orders WHERE status = %s", ['Pending'])
    count_order = cur.fetchone()
    count_orders_where_pending = count_order['COUNT(status)']

    # show new orders
    cur.execute("SELECT COUNT(status), user_name FROM buy_orders WHERE status = %s GROUP BY user_name ASC LIMIT 12", ['Pending'])
    count_orders_by_user = cur.fetchall()

    cur.close()
    return render_template('admin_dashboard.html', count_sliders=count_sliders, count_products=count_products,
                           count_users=count_users, count_categories=count_categories,
                           admin_name=session['admin_username'], admin_image=session['admin_image'],
                           permission=session['permission'], count_number_of_sales=count_number_of_sales,
                           count_number_of_sales_slider=count_number_of_sales_slider, product_saled=product_saled,
                           slider_saled=slider_saled, slider_big=slider_big, slider_small=slider_small,
                           product_big=product_big, product_small=product_small, slider_add=slider_add,
                           product_add=product_add, slider_last_week=slider_last_week,
                           product_last_week=product_last_week, total_avg_rate=total_avg_rate,
                           product_saled_low=product_saled_low, slider_saled_low=slider_saled_low, messages=messages,
                           count_messages=count_messages, count_orders_where_pending=count_orders_where_pending,
                           count_orders_by_user=count_orders_by_user)