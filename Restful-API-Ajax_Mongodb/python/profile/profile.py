# some imports
from flask_mysqldb import MySQL
from python.token_check.check import *

prof = Blueprint('prof', __name__)
mysql = MySQL(app)

# profile route

@prof.route('/users/profile', methods=['post', 'get'])
@token_required
def profile():
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'], app.config['SECRET_KEY'])['username']
        return jsonify({'token': request.headers.get('Authorization'), 'username': username})
