# some imports
from python.database.create_tables import *
from python.default_icon.default_icon import *
# web part
from python.website.home_page.home_page import *
from python.website.home_page.price_range import *
from python.website.home_page.search import *
from python.website.home_page.preview_production import *
from python.website.home_page.preview_production_slider import *
from python.website.home_page.categories import *
from python.website.home_page.all_products import *
from python.website.reset_password.forget_password import *
from python.website.reset_password.email_password import *
from python.website.reset_password.reset_password import *
from python.website.login.register import *
from python.website.login.login import *
from python.website.login.login_check import *
from python.website.login.logout import *
from python.website.home_page.contact_us import *

# user part
from python.user.review.product import *
from python.user.review.slider import *
from python.user.account.account import *
from python.user.account.delete_account import *
from python.user.cart.cart import *
from python.user.cart.buy import *
from python.user.cart.add_product_to_cart import *
from python.user.cart.add_slider_to_cart import *
from python.user.cart.increase_cart_quantity import *
from python.user.cart.decrease_cart_quantity import *
from python.user.cart.edit_cart_quantity import *
from python.user.cart.delete_from_cart import *
from python.user.account.user_profile_picture import *


# admin part
from python.admin.login.login import *
from python.admin.login.login_check import *
from python.admin.login.logout import *
from python.admin.dashboard.dashboard import *
from python.admin.dashboard.admin_search import *
from python.admin.dashboard.upload_profile_picture import *
from python.admin.products.add_product.add import *
from python.admin.products.edit_product.edit import *
from python.admin.products.delete_product.delete import *
from python.admin.products.delete_all_products.delete_all import *
from python.admin.sliders.add_slider.add import *
from python.admin.sliders.edit_slider.edit import *
from python.admin.sliders.delete_slider.delete import *
from python.admin.sliders.delete_all_sliders.delete_all import *
from python.admin.account.add_account.add import *
from python.admin.account.delete_account.delete import *
from python.admin.account.delete_all_users.delete_all_users import *
from python.admin.account.delete_all.delete_all import *
from python.admin.categories.add_category.add import *
from python.admin.categories.edit_category.edit import *
from python.admin.categories.delete_category.delete import *
from python.admin.categories.delete_all_categories.delete_all import *
from python.admin.tables.products_table.products import *
from python.admin.tables.sliders_table.sliders import *
from python.admin.tables.categories_table.categories import *
from python.admin.tables.users_table.users import *
from python.admin.tables.orders_table.orders import *
from python.admin.tables.review_products_table.review_products import *
from python.admin.tables.review_sliders_table.review_sliders import *
from python.admin.tables.orders_table.accept_order import *
from python.admin.tables.orders_table.accept_all import *
from python.admin.tables.orders_table.reject_order import *
from python.admin.tables.orders_table.reject_all import *
from python.admin.tables.review_products_table.delete_review import *
from python.admin.tables.review_products_table.delete_all_reviews import *
from python.admin.tables.review_sliders_table.delete_review import *
from python.admin.tables.review_sliders_table.delete_all_reviews import *
from python.admin.tables.products_table.show_product import *
from python.admin.tables.sliders_table.show_slider import *
from python.admin.tables.messages_table.messages import *
from python.admin.tables.messages_table.delete_all import *
from python.admin.tables.messages_table.delete_all_seen import *
from python.admin.tables.messages_table.delete_all_not_seen import *
from python.admin.tables.messages_table.show_message import *
from python.admin.tables.messages_table.delete_message import *
from python.admin.tables.orders_table.show_orders_by_user import *
from python.admin.tables.orders_table.accept_order_by_user import *
from python.admin.tables.orders_table.accept_all_orders_by_user import *
from python.admin.tables.orders_table.reject_order_by_user import *
from python.admin.tables.orders_table.reject_all_orders_by_user import *


app = Flask(__name__)
# application configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'buy_sell'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


app.register_blueprint(default_icon)

# web part
app.register_blueprint(create_db_tables)
app.register_blueprint(flask_db)
app.register_blueprint(web_home)
app.register_blueprint(web_home_price_range)
app.register_blueprint(search)
app.register_blueprint(product)
app.register_blueprint(slider)
app.register_blueprint(categorie)
app.register_blueprint(all_products)
app.register_blueprint(forget_password)
app.register_blueprint(email_password)
app.register_blueprint(reset_user_password)
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(check)
app.register_blueprint(logout)
app.register_blueprint(contact_us_home_page)

# user part
app.register_blueprint(product_user_review)
app.register_blueprint(slider_user_review)
app.register_blueprint(account)
app.register_blueprint(delete_account)
app.register_blueprint(cart)
app.register_blueprint(user_buy)
app.register_blueprint(add_product)
app.register_blueprint(add_slider)
app.register_blueprint(increase_quantity)
app.register_blueprint(decrease_quantity)
app.register_blueprint(edit_quantity)
app.register_blueprint(delete_from_cart)
app.register_blueprint(profile_picture_for_user)

# admin part

app.register_blueprint(login_admin)
app.register_blueprint(check_admin)
app.register_blueprint(logout_admin)
app.register_blueprint(dashboard)
app.register_blueprint(admin_search)
app.register_blueprint(picture)
app.register_blueprint(add_product_admin)
app.register_blueprint(edit_product_admin)
app.register_blueprint(delete_product_admin)
app.register_blueprint(delete_all_product_admin)
app.register_blueprint(add_slider_admin)
app.register_blueprint(edit_slider_admin)
app.register_blueprint(delete_slider_admin)
app.register_blueprint(delete_all_slider_admin)
app.register_blueprint(add_user_admin)
app.register_blueprint(delete_user_admin)
app.register_blueprint(delete_all_users_admin)
app.register_blueprint(delete_all_admin)
app.register_blueprint(add_category_admin)
app.register_blueprint(edit_category_admin)
app.register_blueprint(delete_category_admin)
app.register_blueprint(delete_all_categories_admin)
app.register_blueprint(products_table_admin)
app.register_blueprint(sliders_table_admin)
app.register_blueprint(categories_table_admin)
app.register_blueprint(users_table_admin)
app.register_blueprint(orders_table_admin)
app.register_blueprint(review_products_table_admin)
app.register_blueprint(review_sliders_table_admin)
app.register_blueprint(accept_order_admin)
app.register_blueprint(accept_all_orders_admin)
app.register_blueprint(reject_order_admin)
app.register_blueprint(reject_all_orders_admin)
app.register_blueprint(delete_review_admin)
app.register_blueprint(delete_all_reviews_admin)
app.register_blueprint(delete_slider_review_admin)
app.register_blueprint(admin_delete_all_slider_reviews)
app.register_blueprint(admin_show_product)
app.register_blueprint(admin_show_slider)
app.register_blueprint(messages_table_admin)
app.register_blueprint(delete_all_messages_admin)
app.register_blueprint(delete_all_seen_messages_admin)
app.register_blueprint(delete_all_not_seen_messages_admin)
app.register_blueprint(show_message_admin)
app.register_blueprint(delete_message_admin)
app.register_blueprint(show_orders_by_user_admin)
app.register_blueprint(accept_order_by_user_admin)
app.register_blueprint(accept_all_order_by_user_admin)
app.register_blueprint(reject_order_by_user_admin)
app.register_blueprint(reject_all_orders_by_user_admin)



# run whole application function

if __name__ == '__main__':
    app.secret_key = 'osama_blog'
    app.run(debug=True)