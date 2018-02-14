# some imports
from flask import make_response
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from cerberus import Validator
import datetime
from python.token_check.check import *


user_login = Blueprint('user_login', __name__)
mysql = MySQL(app)


# register validator schema

schema = {'username': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 100},
          'password': {'required': True, 'type': 'string', 'minlength': 1, 'maxlength': 10}}


# login route

@user_login.route('/users/login', methods=['post', 'get'])
def login():
    v = Validator(schema)
    if request.method == 'POST' and v.validate(request.get_json(), schema) is True:
        username = request.json['username']
        password_candidate = request.json['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = BINARY %s", [username])
        if result > 0:
            data = cur.fetchone()
            cur.close()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                auth = request.authorization
                if auth and auth.password == password_candidate and auth.username == username:
                    token = jwt.encode({'username': auth.username, 'exp': datetime.datetime.utcnow() +\
                                         datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                    return jsonify({'token': token.decode('UTF-8')})
                return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})
            else:
                return jsonify({'Login': False, 'errors': v.errors if v.errors != {} else 'no errors'})
        else:
            return jsonify({'message': 'username not found'})
    return jsonify({'Login': "general", 'errors': v.errors if v.errors != {} else 'no errors'})
