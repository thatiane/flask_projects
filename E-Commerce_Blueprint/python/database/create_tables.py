# some imports
from flask import Blueprint, Flask
import MySQLdb
from passlib.hash import sha256_crypt
from shutil import copy
import os

create_db_tables = Blueprint('create_db_tables', __name__)

# connect to database in localhost to create database and their tables

database = MySQLdb.connect("localhost", "OSAMA", "OSAMA")
cursor = database.cursor()
# cursor.execute("DROP DATABASE IF EXISTS buy_sell;")
cursor.execute("CREATE DATABASE IF NOT EXISTS buy_sell DEFAULT CHARSET UTF8")
database.select_db('buy_sell')
# cursor.execute("DROP TABLE IF EXISTS users;")
# cursor.execute("DROP TABLE IF EXISTS categories;")
# cursor.execute("DROP TABLE IF EXISTS products;")
# cursor.execute("DROP TABLE IF EXISTS slider_products;")
# cursor.execute("DROP TABLE IF EXISTS buy_orders;")
# cursor.execute("DROP TABLE IF EXISTS orders;")
# cursor.execute("DROP TABLE IF EXISTS reviews;")
# cursor.execute("DROP TABLE IF EXISTS slider_reviews;")
# cursor.execute("DROP TABLE IF EXISTS contact_us;")


cursor.execute("CREATE TABLE IF NOT EXISTS users(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                permission VARCHAR(10) NOT NULL,\
                first_name VARCHAR(100) NOT NULL,\
                last_name VARCHAR(100) NOT NULL,\
                email VARCHAR(100) NOT NULL,\
                gender VARCHAR(10) NOT NULL,\
                country VARCHAR(50) NOT NULL,\
                username VARCHAR(100) NOT NULL,\
                password VARCHAR(100) NOT NULL,\
                reset_password_permission VARCHAR(12) NOT NULL,\
                files TEXT NOT NULL,\
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP );")

cursor.execute("CREATE TABLE IF NOT EXISTS products(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                category VARCHAR(100) NOT NULL,\
                number_of_sales INT(11) NOT NULL,\
                number_of_views INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                description TEXT NOT NULL,\
                price INT(11) NOT NULL,\
                discount FLOAT NOT NULL,\
                quantity INT(11) NOT NULL,\
                files TEXT NOT NULL,\
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS slider_products(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                category VARCHAR(100) NOT NULL,\
                number_of_sales INT(11) NOT NULL,\
                number_of_views INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                description TEXT NOT NULL,\
                price INT(11) NOT NULL,\
                discount FLOAT NOT NULL,\
                quantity INT(11) NOT NULL,\
                files TEXT NOT NULL,\
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS categories (category VARCHAR(255) PRIMARY KEY,\
                number_of_products INT(11) NOT NULL);")

cursor.execute("CREATE TABLE IF NOT EXISTS orders(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                user_id INT(11) NOT NULL,\
                user_name VARCHAR(255) NOT NULL,\
                status VARCHAR(255) NOT NULL,\
                product_id INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                quantity INT(11) NOT NULL,\
                price INT(11) NOT NULL,\
                discount FLOAT NOT NULL,\
                files TEXT NOT NULL,\
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS reviews(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                user_id INT(11) NOT NULL,\
                user_name VARCHAR(255) NOT NULL,\
                product_id INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                rate TINYINT(2) NOT NULL,\
                review TEXT NOT NULL,\
                review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS buy_orders(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                user_id INT(11) NOT NULL,\
                user_name VARCHAR(255) NOT NULL,\
                status VARCHAR(255) NOT NULL,\
                product_id INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                quantity INT(11) NOT NULL,\
                price INT(11) NOT NULL,\
                discount FLOAT NOT NULL,\
                country VARCHAR(255) NOT NULL,\
                region VARCHAR(255) NOT NULL,\
                address VARCHAR(255) NOT NULL,\
                phone_number VARCHAR(255) NOT NULL,\
                comments TEXT NOT NULL,\
                files TEXT NOT NULL,\
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS slider_reviews(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                user_id INT(11) NOT NULL,\
                user_name VARCHAR(255) NOT NULL,\
                product_id INT(11) NOT NULL,\
                product_name VARCHAR(255) NOT NULL,\
                rate TINYINT(2) NOT NULL,\
                review TEXT NOT NULL,\
                review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS contact_us(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                status VARCHAR(10) NOT NULL,\
                username VARCHAR(255) NOT NULL,\
                phone VARCHAR(255) NOT NULL,\
                email VARCHAR(255) NOT NULL,\
                message TEXT NOT NULL,\
                write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")


app = Flask(__name__)

# create default admin account if not exists

result = cursor.execute('SELECT username FROM users WHERE username=%s', ['admin'])
if result > 0:
    pass
else:
    admin_password = sha256_crypt.encrypt(str('admin'))
    cursor.execute("INSERT INTO users(permission, first_name, last_name,\
             email, gender, country, username, password, files)\
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            ('admin', 'admin', 'admin', 'admin', 'admin', \
             'admin', 'admin', admin_password, 'admin.png'))
    database.commit()
    try:
        os.makedirs(app.root_path + r"\static\uploads\users\admin")
        copy(app.root_path + r'\static\admin.png', app.root_path + r'\static\uploads\users\admin\admin.png')
    except:
        pass

database.close()