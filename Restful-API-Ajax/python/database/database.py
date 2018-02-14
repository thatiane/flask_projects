
from flask import Flask, Blueprint
import MySQLdb

app = Flask(__name__)
db = Blueprint('db', __name__)



# connect to database in localhost to create database and their tables

database = MySQLdb.connect("localhost", "OSAMA", "OSAMA")
cursor = database.cursor()
# cursor.execute("DROP DATABASE IF EXISTS restful_api;")
cursor.execute("CREATE DATABASE IF NOT EXISTS restful_api DEFAULT CHARSET UTF8")
database.select_db('restful_api')
cursor.execute("CREATE TABLE IF NOT EXISTS users(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                username VARCHAR(100) NOT NULL,\
                email VARCHAR(100) NOT NULL,\
                password VARCHAR(100) NOT NULL,\
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

database.close()