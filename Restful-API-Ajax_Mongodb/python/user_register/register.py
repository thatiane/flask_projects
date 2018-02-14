# some imports
from wtforms import Form, StringField, validators, PasswordField
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from cerberus import Validator
from python.token_check.check import *


user_register = Blueprint('user_register', __name__)
mysql = MySQL(app)


# register validator schema

schema = {'username': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'email': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'password': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 10},
          'confirm': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100}}


# register route

@user_register.route('/users/register', methods=['post', 'get'])
def register():
    v = Validator(schema)

    username = request.json['username']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    cur.close()
    if result == 0:
        if request.method == 'POST' and v.validate(request.get_json(), schema) is True and request.json['password'] == request.json['confirm']:
            username = request.json['username']
            email = request.json['email']
            password = sha256_crypt.encrypt(str(request.json['password']))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", \
                        (username, email, password))
            mysql.connection.commit()
            cur.close()
            return jsonify({'success': True})
        return jsonify({'success': False, 'errors': v.errors if v.errors != {} else '' + 'password not matched' if request.json['password'] != request.json['confirm'] else 'no errors'})
    else:
        return jsonify({'message': 'username already exists', 'errors': v.errors if v.errors != {} else '' + 'password not matched' if request.json['password'] != request.json['confirm'] else 'no errors'})


# request.json['username']
# request.get_json()
