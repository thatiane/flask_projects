# some imports
from flask import request, jsonify, Blueprint, Flask
from functools import wraps
import jwt

app = Flask(__name__)
check = Blueprint('check', __name__)
app.config['SECRET_KEY'] = 'hfhkydkdyfkhfkydchckydfckchcdfkydfykck'


# check if token is still valid

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated
