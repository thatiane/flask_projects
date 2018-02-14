
from flask import Flask, Blueprint
from flask_pymongo import PyMongo, pymongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'restful_api'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restful_api'


dbb = Blueprint('dbb', __name__)



# connect to database in localhost to create database and their tables
mongo = PyMongo(app)
