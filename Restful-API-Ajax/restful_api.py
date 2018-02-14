# some imports

from python.token_check.check import *
from python.add_product.add import *
from python.database.database import *
from python.user_register.register import *
from python.user_login.login import *
from python.all_products.all import *
from python.product.product import *
from python.profile.profile import *
from python.catigories.categories import *
from python.delete_product.delete import *
from python.edit_product.edit import *


app = Flask(__name__)


# secret key over here and token_check only
app.config['SECRET_KEY'] = 'hfhkydkdyfkhfkydchckydfckchcdfkydfykck'


# application configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'restful_api'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=['get'])
def home():
    return render_template('home.html')


app.register_blueprint(check)
app.register_blueprint(add_product_bluprint)
app.register_blueprint(db)
app.register_blueprint(user_register)
app.register_blueprint(user_login)
app.register_blueprint(all_productss)
app.register_blueprint(one_product)
app.register_blueprint(prof)
app.register_blueprint(category)
app.register_blueprint(delete_product_bluprint)
app.register_blueprint(edit_product_bluprint)







if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/loginn')
# def loginn():
#     auth = request.authorization
#     if auth and auth.password == 'secret':
#         token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=90)}, app.config['SECRET_KEY'])
#         return jsonify({'token': token.decode('UTF-8')})
#     return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})


# to check if token has been expired or not
# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'Only available for people that they have a valid token!'})



# print(request.headers.get('Authorization'))
# print(request.headers['Authorization'])
# print(request.headers)