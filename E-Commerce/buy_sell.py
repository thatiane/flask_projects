# some imports
from flask import Flask, render_template, flash, redirect, url_for, session, request, send_from_directory, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators, FileField, IntegerField, PasswordField
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from shutil import rmtree, copyfile, copy2, copy, copyfileobj
from functools import wraps
from flask_mail import Mail, Message
import MySQLdb
import os
import random
import string
import getip


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
                reset_password_random VARCHAR(255) NOT NULL,\
                files TEXT NOT NULL,\
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP );")

cursor.execute("CREATE TABLE IF NOT EXISTS products(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                category VARCHAR(100) NOT NULL,\
                number_of_sales INT(11) NOT NULL,\
                number_of_views INT(11) NOT NULL,\
                avg_rate FLOAT NOT NULL,\
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
                avg_rate FLOAT NOT NULL,\
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
             email, gender, country, username, password, reset_password_permission, files)\
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            ('admin', 'admin', 'admin', 'admin', 'admin', \
             'admin', 'admin', admin_password, 'no_reset', 'admin.png'))
    database.commit()
    try:
        os.makedirs(app.root_path + "/static/uploads/users/admin")
        copy(app.root_path + '/static/admin.png', app.root_path + '/static/uploads/users/admin/admin.png')
    except:
        pass

database.close()


# application configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'buy_sell'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# application configuration to send email with gmail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'osama.buy.sell@gmail.com'
app.config['MAIL_PASSWORD'] = 'chnuxoeikqtyeclg'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# website icon

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'admin.png', mimetype='image/vnd.microsoft.icon')


# page not found route

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# add to compare route

lis = []
@app.route('/add_to_compare/<id>', methods=['post', 'get'])
def add_to_compare(id):
    if len(lis) <= 3:
        lis.append(id)
        session['ids'] = lis
        print(session['ids'])
        flash('added successfully to compare!', 'success')
        return redirect(request.referrer)
    else:
        flash('not added because the limit is reached (4 products only!)', 'danger')
        return redirect(request.referrer)


# compare page

@app.route('/compare')
def compare():
    id1 = session['ids'][0]
    id2 = session['ids'][1]
    id3 = session['ids'][2]
    id4 = session['ids'][3]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", [id1])
    result1 = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE id = %s", [id2])
    result2 = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE id = %s", [id3])
    result3 = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE id = %s", [id4])
    result4 = cur.fetchone()
    cur.close()
    return jsonify(result1, result2, result3, result4)


# home page

@app.route('/', methods=['post', 'get'])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products LIMIT 1")
    slider_products_first = cur.fetchall()
    cur.execute("SELECT * FROM slider_products LIMIT 1 OFFSET 1")
    slider_products_second = cur.fetchall()
    # cur.execute("SELECT * FROM slider_products ORDER BY id DESC LIMIT 1")
    cur.execute("SELECT * FROM slider_products LIMIT 1 OFFSET 2")
    slider_products_third = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 6;")
    latest_products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY number_of_views DESC LIMIT 3;")
    recommended_products = cur.fetchall()
    cur.execute("SELECT * FROM products ORDER BY number_of_views DESC LIMIT 3 OFFSET 3")
    recommended_products_second = cur.fetchall()
    cur.close()

    return render_template('home.html', latest_products=latest_products, categories=categories, slider_products_first=slider_products_first, slider_products_second=slider_products_second, slider_products_third=slider_products_third, recommended_products=recommended_products, recommended_products_second=recommended_products_second)


# contact us form validators

class Contact_us(Form):
    name = StringField('Name', [validators.DataRequired()])
    mobile_phone = StringField('Phone', [validators.DataRequired()])
    email = StringField('E-mail', [validators.DataRequired()])
    message = TextAreaField('Message', [validators.DataRequired()])


# contact us form from home page

@app.route('/contact_us', methods=['post', 'get'])
def contact_us():
    form = Contact_us(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile_phone = form.mobile_phone.data
        # email = form.email.data
        email = request.form['email']
        message = form.message.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact_us(status, username, phone, email, message)\
                     VALUES(%s, %s, %s, %s, %s)", ("not_seen", name, mobile_phone, email, message))
        mysql.connection.commit()
        cur.close()
        flash("Your Message has been Sent to Us successfully!", "success")
        return redirect(url_for('home'))
    return render_template('contact_us.html', form=form)


# products range price

@app.route('/products_price_range', methods=['post', 'get'])
def products_price_range():
    # min_price = request.form['price'].split(',')[0]
    # max_price = request.form['price'].split(',')[1]
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM products WHERE (price BETWEEN %s AND %s)", [min_price, max_price])
    cur.close()
    if result > 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE (price BETWEEN %s AND %s)", [min_price, max_price])
        search_products = cur.fetchall()
        cur.close()
        return render_template('user_search.html', search_products=search_products)
    else:
        flash('No Products Found', 'warning')
        return render_template('user_search.html')


# all products page

@app.route('/products/<id>')
def products(id):
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM products ORDER BY id DESC;")
    # all_products = cur.fetchall()

    cur.execute("SELECT COUNT(id) FROM products ORDER BY id ASC;")
    pr = cur.fetchone()
    number_of_products = int(pr['COUNT(id)'] / 10)

    off = (int(id) * 10) - 10
    cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 10 OFFSET %s;", [off])
    all_products = cur.fetchall()


    # for product in all_products:
    #     product_name = product['product_name']
    #     print(product_name)
    #     cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_name = %s;", [product_name])
    #     rate = cur.fetchall()
    #     print(rate)
    cur.close()
    return render_template('all_products.html', all_products=all_products, number_of_products=number_of_products)


# user reset password page

@app.route('/user_forget_password')
def user_forget_password():
    return render_template('user_forget_password.html')


# send e-mail with link to reset user account password

@app.route("/user_forget_password_email", methods=['GET', 'POST'])
def user_forget_password_email():
    if request.form['username_reset'] == '':
        flash('You did not write a username !', 'warning')
        return render_template('user_forget_password.html')
    user_name = request.form['username_reset']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT id, email, username FROM users WHERE username = BINARY %s AND permission='user' ", [user_name])
    res = cur.fetchone()
    if r > 0:
        random_for_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
        email = res['email']
        msg = Message()
        msg.sender = 'osama.buy.sell@gmail.com'
        msg.subject = "Reset Your Password"
        msg.recipients = [email]
        msg.body = "Reset Your Password : http://localhost:5000/user_reset_password/%s/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'], random_for_reset)
        mail.send(msg)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET reset_password_permission = 'reset',  reset_password_random = %s WHERE username = %s AND permission='user'", [random_for_reset, user_name])
        mysql.connection.commit()
        cur.close()
        flash("The Reset Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('home'))
    else:
        cur.close()
        flash("This username Not Found!", "warning")
        return redirect(url_for('home'))


# reset password form validators

class reset_password(Form):
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# write new password page

@app.route("/user_reset_password/<id>/<random_for_reset>", methods=['GET', 'POST'])
def user_reset_password(id, random_for_reset):
    form = reset_password(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        cur.execute("SELECT reset_password_permission, reset_password_random FROM users WHERE id = %s AND permission='user'", [id])
        permission = cur.fetchone()
        password_permission = permission['reset_password_permission']
        reset_random = permission['reset_password_random']
        if password_permission == 'reset' and random_for_reset == reset_random:
            random_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
            encrypted_password = sha256_crypt.encrypt(str(form.password.data))
            cur.execute("UPDATE users SET password = %s WHERE id = %s AND permission='user'", [encrypted_password, id])
            cur.execute("UPDATE users SET reset_password_permission = 'no_reset', reset_password_random = %s WHERE id = %s AND permission='user'", [random_reset, id])
            mysql.connection.commit()
            cur.close()
            flash("You Have Successfully Changed Your Password Now!", "success")
            return redirect(url_for('home'))
        else:
            cur.close()
            flash("You Have Changed Your Password before!", "warning")
            return redirect(url_for('home'))
    return render_template('user_reset_password.html', form=form)


# user part ***********************************************************************************************


# user registration validators form

class RegisterForm(Form):
    first_name = StringField('First Name', [validators.InputRequired()])
    last_name = StringField('Last Name', [validators.InputRequired()])
    username = StringField('User Name', [validators.InputRequired()])
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords Do Not Match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# user register page

@app.route('/user_register', methods=['post', 'get'])
def user_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data

        folder = os.path.exists(app.root_path + "/static/uploads/users/{}".format(username))
        if folder == True:
            flash('Folder Name Already Exists', 'warning')
            return redirect(url_for('user_register'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", [username])
        res = cur.fetchone()
        if username in str(res):
            cur.close()
            msg = "User Name Already Exists"
            return render_template('user_register.html', form=form, msg=msg)
        else:
            cur.close()
            first_name = form.first_name.data.lower()
            last_name = form.last_name.data.lower()
            email = request.form['email'].lower()
            gender = request.form['gender']
            country = request.form['country']
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))
            file = request.files['file']
            # if file.filename == '':
            #     flash('You Have to Select a File!', 'warning')
            if file and allowed_file(file.filename):
                try:
                    rmtree(app.root_path + "/static/uploads/users/{}".format(username))
                    os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
                except:
                    os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
                filename = secure_filename(file.filename)
                dir = app.root_path + "/static/uploads/users/{}".format(username)
                file.save(os.path.join(dir, filename))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                             email, gender, country, username, password, reset_password_permission, files)\
                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            ("user", first_name, last_name, email, gender,\
                             country, username, password, 'no_reset', filename))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created Account successfully!', 'success')
                return redirect(url_for('user_login'))
            elif file.filename == '' or 'file' not in request.files:
                try:
                    rmtree(app.root_path + "/static/uploads/users/{}".format(username))
                    os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
                except:
                    os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
                copy(app.root_path + '/static/admin.png', app.root_path + '/static/uploads/users/{}/admin.png'.format(username))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                                             email, gender, country, username, password, reset_password_permission, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            ("user", first_name, last_name, email, gender, \
                             country, username, password, 'no_reset', 'admin.png'))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created Account successfully!', 'success')
                return redirect(url_for('user_login'))
    return render_template('user_register.html', form=form)


# user login page

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = BINARY %s AND permission='user'", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['user_logged_in'] = True
                session['user_username'] = username
                cur.close()
                flash('Now You Are Logged In ', 'success')
                return redirect(url_for('user_account'))
            else:
                cur.close()
                error = 'Wrong Password!'
                return render_template('user_login.html', error=error)
        else:
            cur.close()
            error = 'Username Can Not Be Found!'
            return render_template('user_login.html', error=error)
    return render_template('user_login.html')


# check if user is still logged in 

def is_user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('user_login'))
    return wrap


# user log out

@app.route('/user_logout')
@is_user_logged_in
def user_logout():
    session.clear()
    flash('You Are Now Logged Out', 'success')
    return redirect(url_for('user_login'))


# user account page

@app.route('/user_account', methods=['post', 'get'])
@is_user_logged_in
def user_account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buy_orders WHERE user_name = %s", [session['user_username']])
    orders = cur.fetchall()
    cur.execute("SELECT files FROM users WHERE username = %s", [session['user_username']])
    image = cur.fetchone()
    user_image = image['files']
    cur.close()
    return render_template('user_account.html', orders=orders, user_image=user_image)


# upload user profile picture

@app.route('/user_profile_picture', methods=['post'])
@is_user_logged_in
def user_profile_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(url_for('user_account'))
        file = request.files['file']
        if file.filename == '':
            flash('You Have to Select a File!', 'warning')
            return redirect(url_for('user_account'))
        if file and allowed_file(file.filename):
            try:
                rmtree(app.root_path + "/static/uploads/users/{}".format(session['user_username']))
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(session['user_username']))
            except:
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(session['user_username']))
            filename = secure_filename(file.filename)
            dir = app.root_path + "/static/uploads/users/{}".format(session['user_username'])
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET files = %s WHERE username = %s AND permission = %s;", [filename, session['user_username'], 'user'])
            mysql.connection.commit()
            cur.close()
            flash('You Have successfully uploaded Your Profile Picture!', 'success')
            return redirect(url_for('user_account'))
    return redirect(url_for('user_account'))


# user change password form validators

class userchange_password(Form):
    old_password = PasswordField('Old Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100)])
    password = PasswordField('New Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# admin change password page

@app.route("/user_change_password/", methods=['GET', 'POST'])
@is_user_logged_in
def user_change_password():
    form = userchange_password(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s AND permission='user'", [session['user_username']])
        check_password = cur.fetchone()
        cur.close()
        current_password = check_password['password']
        if sha256_crypt.verify(form.old_password.data, current_password):
            cur = mysql.connection.cursor()
            cur.execute("SELECT reset_password_permission, reset_password_random FROM users WHERE username = %s AND permission='user'", [session['user_username']])
            permission = cur.fetchone()
            cur.close()
            password_permission = permission['reset_password_permission']
            if password_permission == 'reset' or password_permission == 'no_reset':
                random_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
                encrypted_password = sha256_crypt.encrypt(str(form.password.data))
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET password = %s WHERE username = %s AND permission='user'", [encrypted_password, session['user_username']])
                cur.execute("UPDATE users SET reset_password_permission = 'no_reset', reset_password_random = %s WHERE username = %s AND permission='user'", [random_reset, session['user_username']])
                mysql.connection.commit()
                cur.close()
                session.clear()
                flash("You Have Successfully Changed Your Password Now!", "success")
                return redirect(url_for('user_login'))
        else:
            flash("You Have Entered a wrong old Password!", "danger")
            return redirect(url_for('user_change_password'))
    return render_template('user_change_password.html', form=form)


# delete user account

@app.route('/delete_user_account', methods=['post', 'get'])
@is_user_logged_in
def delete_user_account():
    rmtree(app.root_path + "/static/uploads/users/{}".format(session['user_username']))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM buy_orders WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM reviews WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM slider_reviews WHERE user_name = %s", [session['user_username']])
    cur.execute("DELETE FROM users WHERE username = %s", [session['user_username']])
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('You Have Deleted Your Account successfully!', 'success')
    return redirect(url_for('home'))


# user registration validators form

class CartbuyForm(Form):
    address = StringField('Address', [validators.InputRequired(), validators.length(min=10, max=200)])
    phone_number = IntegerField('Phone Number', [validators.InputRequired()])
    comments = TextAreaField('Comments', [validators.InputRequired()])


# cart page

@app.route('/add_to_cart', methods=['post', 'get'])
@is_user_logged_in
def add_to_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
    orders = cur.fetchall()
    cur.execute("SELECT user_name FROM orders WHERE user_name = %s", [session['user_username']])
    f = cur.fetchall()
    cur.execute("SELECT SUM((price * quantity) - (quantity * discount)) FROM orders WHERE user_name = %s", [session['user_username']])
    # cur.execute("SELECT SUM((price * quantity) - (quantity * discount)) AS total FROM orders WHERE user_name = %s", [session['user_username']])
    order_price = cur.fetchone()
    cur.execute("SELECT SUM(quantity) FROM orders WHERE user_name = %s", [session['user_username']])
    quantities = cur.fetchone()
    cur.close()
    return render_template('cart.html', orders=orders, price=order_price['SUM((price * quantity) - (quantity * discount))'], quantity=quantities['SUM(quantity)'], f=f)


# buy orders page

@app.route('/buy', methods=['post', 'get'])
@is_user_logged_in
def buy():
    cur = mysql.connection.cursor()
    nat = cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
    if nat > 0:
        cur.close()
        form = CartbuyForm(request.form)
        if request.method == 'POST' and form.validate():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
            buy_orders = cur.fetchall()
            for order in buy_orders:
                user_id = order['user_id']
                user_name = order['user_name']
                product_id = order['product_id']
                product_name = order['product_name']
                quantity = order['quantity']
                price = order['price']
                discount = order['discount']
                files = order['files']
                cur.execute("INSERT INTO buy_orders(user_id, user_name, status, product_id, product_name,\
                                                                quantity, price, discount, files)\
                                                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (user_id, user_name, 'Pending', product_id, product_name, \
                             quantity, price, discount, files))
                mysql.connection.commit()
            result = cur.execute("SELECT country FROM buy_orders WHERE country = '' AND user_name = %s", [session['user_username']])
            if result > 0:
                country = request.form['country']
                region = request.form['region']
                address = form.address.data
                phone_number = form.phone_number.data
                comments = form.comments.data
                cur.execute("UPDATE buy_orders SET country = %s, region = %s, address = %s, phone_number = %s, comments = %s WHERE  country = '' AND user_name = %s", \
                    [country, region, address, phone_number, comments, session['user_username']])

                cur.execute("SELECT * FROM orders WHERE user_name = %s", [session['user_username']])
                confirm_orders = cur.fetchall()
                for confirm_order in confirm_orders:
                    product_name = confirm_order['product_name']
                    quantity = confirm_order['quantity']
                    cur.execute("UPDATE products SET number_of_sales = number_of_sales + 1 WHERE product_name = %s", [product_name])
                    cur.execute("UPDATE products SET quantity = quantity - %s WHERE product_name = %s", [quantity, product_name])
                    mysql.connection.commit()

                for confir_order in confirm_orders:
                    produc_name = confir_order['product_name']
                    quantity = confir_order['quantity']
                    cur.execute("UPDATE slider_products SET number_of_sales = number_of_sales + 1 WHERE product_name = %s", [produc_name])
                    cur.execute("UPDATE slider_products SET quantity = quantity - %s WHERE product_name = %s", [quantity, produc_name])
                    mysql.connection.commit()

                cur.execute("DELETE FROM orders WHERE user_name = %s", [session['user_username']])
                mysql.connection.commit()
                cur.close()
                flash('Your order is successfully sent!', 'success')
                return redirect(url_for('home'))
            elif result == 0:
                cur.close()
                flash('you can not be able to buy until you add product to your cart', 'danger')
                return redirect(url_for('add_to_cart'))
        return render_template('buy.html', form=form)
    elif nat == 0:
        cur.close()
        flash('you can not be able to buy until you add product to your cart', 'danger')
        return redirect(url_for('add_to_cart'))


# add product to the cart

@app.route('/add_product_to_cart/<id>', methods=['post', 'get'])
@is_user_logged_in
def add_product_to_cart(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT product_name FROM orders WHERE product_id = %s AND user_name = %s ", [id, session['user_username']])
    if result > 0:
        cur.close()
        flash('You can not add this product because its already added before!', 'danger')
        return redirect(url_for('add_to_cart'))
    if result == 0:
        cur.execute("SELECT * FROM products WHERE id = %s", [id])
        product = cur.fetchone()
        product_id = product['id']
        product_name = product['product_name']
        product_price = product['price']
        product_discount = product['discount']
        product_files = product['files']
        user_name = session['user_username']
        cur.execute("SELECT id FROM users WHERE username = %s", [session['user_username']])
        res = cur.fetchone()
        user_id = res['id']
        cur.execute("INSERT INTO orders(user_id, user_name, status, product_id, quantity,\
                                     product_name, price, discount, files)\
                                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                    (user_id, user_name, 'Pending', product_id, 1, product_name, \
                     product_price, product_discount, product_files))
        mysql.connection.commit()
        cur.close()
        flash('Added successfully to your cart', 'success')
        return redirect(url_for('add_to_cart'))
    return redirect(url_for('home'))


# add product to the cart from slider

@app.route('/add_product_to_cart_from_slider/<id>', methods=['post', 'get'])
@is_user_logged_in
def add_product_to_cart_from_slider(id):
    cur = mysql.connection.cursor()

    proid = (int(id) * int(-1))
    result = cur.execute("SELECT product_name FROM orders WHERE product_id = %s AND user_name = %s ", [proid, session['user_username']])
    if result > 0:
        cur.close()
        flash('You can not add this product because its already added before!', 'danger')
        return redirect(url_for('add_to_cart'))
    if result == 0:
        cur.execute("SELECT * FROM slider_products WHERE id = %s", [id])
        product = cur.fetchone()
        # product_id = product['id']
        product_id = (int(product['id']) * int(-1))
        product_name = product['product_name']
        product_price = product['price']
        product_discount = product['discount']
        product_files = product['files']
        user_name = session['user_username']
        cur.execute("SELECT id FROM users WHERE username = %s", [session['user_username']])
        res = cur.fetchone()
        user_id = res['id']
        cur.execute("INSERT INTO orders(user_id, user_name, status, product_id, quantity,\
                                     product_name, price, discount, files)\
                                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                    (user_id, user_name, 'Pending', product_id, 1, product_name, \
                     product_price, product_discount, product_files))
        mysql.connection.commit()
        cur.close()
        flash('Added successfully to your cart', 'success')
        return redirect(url_for('add_to_cart'))
    return redirect(url_for('home'))


# increase cart product quantity in cart page

@app.route('/increase_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def increase_cart_product_quantity(id):
    cur = mysql.connection.cursor()
    if int(id) > 0:
        cur.execute("SELECT quantity FROM products WHERE id = %s", [id])
        result = cur.fetchone()
        product_quantity = result['quantity']
    elif int(id) < 0:
        fixid = abs(int(id))
        cur.execute("SELECT quantity FROM slider_products WHERE id = %s", [fixid])
        result = cur.fetchone()
        slider_quantity = result['quantity']
    cur.execute("SELECT quantity FROM orders WHERE product_id = {}".format(id))
    res = cur.fetchone()
    order_quantity = res['quantity']
    cur.close()
    if int(id) > 0:
        if order_quantity <= product_quantity - 1:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE orders SET quantity = quantity + 1 WHERE product_id = {}".format(id))
            mysql.connection.commit()
            cur.close()
            flash('You have updated the product quantity successfully!', 'success')
            return redirect(url_for('add_to_cart'))
        else:
            message = 'You can not put the quantity more than ' + str(product_quantity) + ' products!'
            flash(message, 'danger')
            return redirect(url_for('add_to_cart'))
    else:
        if order_quantity <= slider_quantity - 1:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE orders SET quantity = quantity + 1 WHERE product_id = {}".format(id))
            mysql.connection.commit()
            cur.close()
            flash('You have updated the product quantity successfully!', 'success')
            return redirect(url_for('add_to_cart'))
        else:
            message = 'You can not put the quantity more than ' + str(slider_quantity) + ' products!'
            flash(message, 'danger')
            return redirect(url_for('add_to_cart'))


# edit cart product quantity in cart page

@app.route('/edit_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def edit_cart_product_quantity(id):
    cur = mysql.connection.cursor()
    if int(id) > 0:
        cur.execute("SELECT quantity FROM products WHERE id = %s", [id])
        result = cur.fetchone()
        product_quantity = result['quantity']
    elif int(id) < 0:
        fixid = abs(int(id))
        cur.execute("SELECT quantity FROM slider_products WHERE id = %s", [fixid])
        res = cur.fetchone()
        slider_quantity = res['quantity']
    cur.close()
    quantity = request.form['quantity']
    try:
        if int(quantity) > 0:
            if int(id) > 0:
                if int(quantity) <= product_quantity:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE orders SET quantity = %s WHERE product_id = %s", [quantity, id])
                    mysql.connection.commit()
                    cur.close()
                    flash('You have updated the product quantity successfully!', 'success')
                    return redirect(url_for('add_to_cart'))
                else:
                    message = 'You can not put the quantity more than ' + str(product_quantity) + ' products!'
                    flash(message, 'danger')
                    return redirect(url_for('add_to_cart'))
            else:
                if int(quantity) <= slider_quantity:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE orders SET quantity = %s WHERE product_id = %s", [quantity, id])
                    mysql.connection.commit()
                    cur.close()
                    flash('You have updated the product quantity successfully!', 'success')
                    return redirect(url_for('add_to_cart'))
                else:
                    message = 'You can not put the quantity more than ' + str(slider_quantity) + ' products!'
                    flash(message, 'danger')
                    return redirect(url_for('add_to_cart'))
        else:
            pass
            flash('You can not put the quantity less than one!', 'danger')
            return redirect(url_for('add_to_cart'))
    except ValueError:
        flash('You have to write a right number!', 'danger')
        return redirect(url_for('add_to_cart'))


# decrease cart product quantity in cart page

@app.route('/decrease_cart_product_quantity/<id>', methods=['post', 'get'])
@is_user_logged_in
def decrease_cart_product_quantity(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT quantity FROM orders WHERE product_id = %s", [id])
    cart_product = cur.fetchone()
    product_quantity = cart_product['quantity']
    cur.close()
    if product_quantity <= 1:
        flash('You can not put the quantity less than one!', 'danger')
        pass
    if product_quantity > 1:
        cur.execute("UPDATE orders SET quantity = quantity - 1 WHERE product_id = {}".format(id))
        mysql.connection.commit()
        flash('You have updated the product quantity successfully!', 'success')
    return redirect(url_for('add_to_cart'))


# delete product from cart page

@app.route('/delete_product_from_cart/<id>', methods=['post', 'get'])
@is_user_logged_in
def delete_product_from_cart(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE product_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('You have deleted the product successfully from your cart!', 'success')
    return redirect(url_for('add_to_cart'))


# add product review
@app.route('/product_review/<id>', methods=['post', 'get'])
@is_user_logged_in
def product_review(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT product_id FROM reviews WHERE user_name = %s AND product_id = %s", [session['user_username'], id])
    cur.close()
    if result == 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, product_name FROM products WHERE id = %s", [id])
        product = cur.fetchone()
        product_id = product['id']
        product_name = product['product_name']
        cur.execute("SELECT id, username FROM users WHERE username = %s", [session['user_username']])
        user = cur.fetchone()
        user_id = user['id']
        user_name = user['username']
        cur.close()

        product_rate = request.form['rate']
        review = request.form['product_review_area']

        if review == '':
            flash('You must write a review!', 'danger')
            return redirect(url_for('home'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO reviews(user_id, user_name, product_id, product_name, rate, review)\
                         VALUES(%s, %s, %s, %s, %s, %s)", \
                        (user_id, user_name, product_id, product_name, product_rate, review))
            mysql.connection.commit()
            cur.execute("SELECT SUM(rate) / COUNT(product_id) AS total_avg_rate FROM reviews WHERE product_id = %s", [id])
            total = cur.fetchone()
            total_rate = total['total_avg_rate']
            cur.execute("UPDATE products SET avg_rate = %s WHERE id = %s", [total_rate, id])
            mysql.connection.commit()
            cur.close()
            flash('Your review now added successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('You can not add two reviews for one product!', 'danger')
        return redirect(url_for('home'))


# add slider product review
@app.route('/slider_product_review/<id>', methods=['post', 'get'])
@is_user_logged_in
def slider_product_review(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT product_id FROM slider_reviews WHERE user_name = %s AND product_id = %s", [session['user_username'], id])
    cur.close()
    if result == 0:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, product_name FROM slider_products WHERE id = %s", [id])
        product = cur.fetchone()
        product_id = product['id']
        product_name = product['product_name']
        cur.execute("SELECT id, username FROM users WHERE username = %s", [session['user_username']])
        user = cur.fetchone()
        cur.close()
        user_id = user['id']
        user_name = user['username']

        product_rate = request.form['rate']
        review = request.form['product_review_area']

        if review == '':
            flash('You must write a review!', 'danger')
            return redirect(url_for('home'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO slider_reviews(user_id, user_name, product_id, product_name, rate, review)\
                         VALUES(%s, %s, %s, %s, %s, %s)", \
                        (user_id, user_name, product_id, product_name, product_rate, review))
            mysql.connection.commit()
            cur.execute("SELECT SUM(rate) / COUNT(product_id) AS total_avg_rate FROM slider_reviews WHERE product_id = %s", [id])
            total = cur.fetchone()
            total_rate = total['total_avg_rate']
            cur.execute("UPDATE slider_products SET avg_rate = %s WHERE id = %s", [total_rate, id])
            mysql.connection.commit()
            cur.close()
            flash('Your review now added successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('You can not add two reviews for one product!', 'danger')
        return redirect(url_for('home'))


# A common part between the admin and the user ********************************************************


# preview product page

@app.route('/preview_production/<id>/')
def preview_production(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(product_id) FROM reviews WHERE product_id={}".format(id))
    reviews = cur.fetchone()
    count_reviews = reviews['COUNT(product_id)']

    reviewresult = cur.execute("SELECT * FROM reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    review = cur.fetchone()

    cur.execute("SELECT * FROM products WHERE id={}".format(id))
    product = cur.fetchone()
    cur.execute("SELECT * FROM products WHERE id != %s ORDER BY id DESC LIMIT 6", [id])
    products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("UPDATE products SET number_of_views = number_of_views + 1 WHERE id={}".format(id))
    mysql.connection.commit()

    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

    cur.close()
    return render_template('preview_production.html', product=product, products=products, categories=categories, count_reviews=count_reviews, review=review, reviewresult=reviewresult, rate=rate)


# preview slider product page

@app.route('/preview_production_slider/<id>/')
def preview_production_slider(id):
    cur = mysql.connection.cursor()
    slider_reviewresult = cur.execute("SELECT * FROM slider_reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    slider_review = cur.fetchone()
    cur.execute("SELECT COUNT(product_id) FROM slider_reviews WHERE product_id={}".format(id))
    reviews = cur.fetchone()
    count_reviews = reviews['COUNT(product_id)']

    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM slider_reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

    cur.execute("SELECT * FROM slider_products WHERE id={}".format(id))
    product = cur.fetchone()
    cur.execute("SELECT * FROM slider_products WHERE id != %s ORDER BY id DESC LIMIT 6", [id])
    products = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("UPDATE slider_products SET number_of_views = number_of_views + 1 WHERE id={}".format(id))
    mysql.connection.commit()
    cur.close()
    return render_template('preview_production_slider.html', product=product, products=products, categories=categories, slider_reviewresult=slider_reviewresult, slider_review=slider_review, count_reviews=count_reviews, rate=rate)


# show all products in specific category 

@app.route('/categories/<category>', methods=['post', 'get'])
def categories(category):
    cur = mysql.connection.cursor()
    cur.execute("SELECT category, number_of_products FROM categories")
    all_categories = cur.fetchall()
    result = cur.execute("SELECT * FROM products WHERE category=%s", [category])
    categories = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('catigories.html', categories=categories, all_categories=all_categories)
    else:
        msg = 'No Products Found!'
        return render_template('catigories.html', msg=msg, all_categories=all_categories)


# user search bar

@app.route('/user_search', methods=['GET', 'POST'])
def user_search():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM products \
                             WHERE( CONVERT(`product_name` USING utf8)\
                             LIKE %s)", [["%" + request.form['search'] + "%"]])
        search_products = cur.fetchall()
        cur.close()
        if result > 0:
            return render_template('user_search.html', search_products=search_products)
        else:
            flash('No Products Found', 'warning')
            return render_template('user_search.html')


# admin part ***********************************************************************************************


# user reset password page

@app.route('/admin/admin_forget_password')
def admin_forget_password():
    return render_template('admin_forget_password.html')


# send e-mail with link to reset user account password

@app.route("/admin/admin_forget_password_email", methods=['GET', 'POST'])
def admin_forget_password_email():
    if request.method == 'POST' and request.form['admin_username'] != '':
        user_name = request.form['admin_username']
        cur = mysql.connection.cursor()
        r = cur.execute("SELECT id, email, username FROM users WHERE username = BINARY %s AND permission='admin' OR permission='editor' ", [user_name])
        res = cur.fetchone()
        cur.close()
        if r > 0:
            random_for_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
            email = res['email']
            msg = Message()
            msg.sender = 'osama.buy.sell@gmail.com'
            msg.subject = "Reset Your Password"
            msg.recipients = [email]
            msg.body = "Reset Your Password : http://localhost:5000/admin/admin_reset_password/%s/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'], random_for_reset)
            mail.send(msg)
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET reset_password_permission = 'reset',  reset_password_random = %s WHERE username = %s AND permission='admin' OR permission='editor'", [random_for_reset, user_name])
            mysql.connection.commit()
            cur.close()
            flash("The Reset Message has been Sent to your email!", "success")
            flash("Please check your email!", "warning")
            return redirect(url_for('admin_forget_password'))
        else:
            flash("This username Not Found!", "warning")
            return redirect(url_for('admin_forget_password'))


# reset password form validators

class adminreset_password(Form):
    password = PasswordField('',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('', [validators.DataRequired()])


# write new password page

@app.route("/admin/admin_reset_password/<id>/<random_for_reset>", methods=['GET', 'POST'])
def admin_reset_password(id, random_for_reset):
    form = adminreset_password(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        cur.execute("SELECT reset_password_permission, reset_password_random FROM users WHERE id = %s AND permission='admin' OR permission='editor'", [id])
        permission = cur.fetchone()
        cur.close()
        password_permission = permission['reset_password_permission']
        reset_random = permission['reset_password_random']
        if password_permission == 'reset' and random_for_reset == reset_random:
            random_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
            encrypted_password = sha256_crypt.encrypt(str(form.password.data))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET password = %s WHERE id = %s AND permission='admin' OR permission='editor'", [encrypted_password, id])
            cur.execute("UPDATE users SET reset_password_permission = 'no_reset', reset_password_random = %s WHERE id = %s AND permission='admin' OR permission='editor'", [random_reset, id])
            mysql.connection.commit()
            cur.close()
            flash("You Have Successfully Changed Your Password Now!", "success")
            return redirect(url_for('admin_login'))
        else:
            flash("You Have Changed Your Password before!", "warning")
            return redirect(url_for('admin_login'))
    return render_template('admin_reset_password.html', form=form)


# admin login page

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = BINARY %s AND permission='admin' OR permission='editor'", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                cur.execute("SELECT files, permission FROM users WHERE username = %s", [username])
                files = cur.fetchone()
                image = files['files']
                permission = files['permission']
                session['admin_logged_in'] = True
                session['admin_username'] = username
                session['admin_image'] = image
                session['permission'] = permission
                cur.close()
                flash('Now You Are Logged In ', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                cur.close()
                error = 'Wrong Password!'
                return render_template('admin_login.html', error=error)
        else:
            cur.close()
            error = 'Username Can Not Be Found!'
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')


# check if admin is still logged in 

def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('admin_login'))
    return wrap


# admin log out

@app.route('/admin/logout')
@is_admin_logged_in
def admin_logout():
    session.clear()
    flash('You Are Now Logged Out', 'success')
    return redirect(url_for('admin_login'))


# admin change password form validators

class adminchange_password(Form):
    old_password = PasswordField('Old Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100)])
    password = PasswordField('New Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# admin change password page

@app.route("/admin/admin_change_password/", methods=['GET', 'POST'])
@is_admin_logged_in
def admin_change_password():
    cur = mysql.connection.cursor()

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
    form = adminchange_password(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s AND permission='admin' OR permission='editor'", [session['admin_username']])
        check_password = cur.fetchone()
        cur.close()
        current_password = check_password['password']
        if sha256_crypt.verify(form.old_password.data, current_password):
            cur = mysql.connection.cursor()
            cur.execute("SELECT reset_password_permission, reset_password_random FROM users WHERE username = %s AND permission='admin' OR permission='editor'", [session['admin_username']])
            permission = cur.fetchone()
            cur.close()
            password_permission = permission['reset_password_permission']
            # reset_random = permission['reset_password_random']
            if password_permission == 'reset' or password_permission == 'no_reset' or password_permission == '':
                random_reset = "".join([random.choice(string.ascii_letters + string.digits) for i in range(250)])
                encrypted_password = sha256_crypt.encrypt(str(form.password.data))
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET password = %s WHERE username = %s AND permission='admin' OR permission='editor'", [encrypted_password, session['admin_username']])
                cur.execute("UPDATE users SET reset_password_permission = 'no_reset', reset_password_random = %s WHERE username = %s AND permission='admin' OR permission='editor'", [random_reset, session['admin_username']])
                mysql.connection.commit()
                cur.close()
                session.clear()
                flash("You Have Successfully Changed Your Password Now!", "success")
                return redirect(url_for('admin_login'))
        else:
            flash("You Have Entered a wrong old Password!", "danger")
            return redirect(url_for('admin_change_password'))
    return render_template('admin_change_password.html', form=form, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# delete admin account

@app.route('/admin/delete_admin_account', methods=['post', 'get'])
@is_admin_logged_in
def delete_admin_account():
    rmtree(app.root_path + "/static/uploads/users/{}".format(session['admin_username']))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", [session['admin_username']])
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('You Have Deleted Your Account successfully!', 'success')
    return redirect(url_for('admin_login'))


# admin dashboard page

@app.route('/admin/', methods=['post', 'get'])
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
    cur.execute("SELECT SUM(rate) / COUNT(rate) AS AVG_RATE FROM (SELECT rate FROM slider_reviews UNION ALL SELECT rate FROM reviews) T;")
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
    return render_template('admin_dashboard.html', count_sliders=count_sliders, count_products=count_products, count_users=count_users, count_categories=count_categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], count_number_of_sales=count_number_of_sales, count_number_of_sales_slider=count_number_of_sales_slider, product_saled=product_saled, slider_saled=slider_saled, slider_big=slider_big, slider_small=slider_small, product_big=product_big, product_small=product_small, slider_add=slider_add, product_add=product_add, slider_last_week=slider_last_week, product_last_week=product_last_week, total_avg_rate=total_avg_rate, product_saled_low=product_saled_low, slider_saled_low=slider_saled_low, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin upload profile picture page

@app.route('/admin/upload_picture', methods=['post', 'get'])
@is_admin_logged_in
def upload_picture():
    cur = mysql.connection.cursor()

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
    return render_template('admin_upload_profile_picture.html', admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# upload admin profile picture

@app.route('/admin/admin_profile_picture', methods=['post'])
@is_admin_logged_in
def admin_profile_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(url_for('admin_dashboard'))
        file = request.files['file']
        if file.filename == '':
            flash('You Have to Select a File!', 'warning')
            return redirect(url_for('admin_dashboard'))
        if file and allowed_file(file.filename):
            try:
                rmtree(app.root_path + "/static/uploads/users/{}".format(session['admin_username']))
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(session['admin_username']))
            except:
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(session['admin_username']))
            filename = secure_filename(file.filename)
            dir = app.root_path + "/static/uploads/users/{}".format(session['admin_username'])
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET files = %s WHERE username = %s AND permission = %s ;", [filename, session['admin_username'], session['permission']])
            mysql.connection.commit()
            cur.close()
            flash('You Have successfully uploaded Your Profile Picture!', 'success')
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_dashboard'))


# product validators form

class AddProductForm(Form):
    product_name = StringField('Name Of Product', [validators.InputRequired(), validators.length(min=1, max=180)])
    description = TextAreaField('Description', [validators.InputRequired()])
    price = IntegerField('Price', [validators.InputRequired()])
    discount = StringField('Discount Percentage %')
    quantity = StringField('Quantity', [validators.InputRequired()])
    # files = FileField('Add picture to Your Product', [validators.InputRequired()])


# admin add new product page

@app.route('/admin/add_product', methods=['post', 'get'])
@is_admin_logged_in
def add_product():
    form = AddProductForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()

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
    if result > 0:
        if request.method == 'POST' and form.validate():
            product_name = form.product_name.data

            folder = os.path.exists(app.root_path + "/static/uploads/products/{}".format(product_name))
            if folder == True:
                flash('Folder Name Already Exists', 'warning')
                return redirect(url_for('add_product'))
            cur = mysql.connection.cursor()
            cur.execute("SELECT product_name FROM products WHERE product_name = %s", [product_name])
            res = cur.fetchone()
            if product_name in str(res):
                msg = "Product Name Already Exists"
                return render_template('admin_add_production.html', form=form, msg=msg, admin_name=session['admin_username'], admin_image=session['admin_image'])

            if request.method == 'POST' and form.validate():
                file = request.files['file']
                if file.filename == '':
                    flash('You Have to Select a File!', 'warning')
                if file and allowed_file(file.filename):
                    try:
                        rmtree(app.root_path + "/static/uploads/products/{}".format(product_name))
                        os.makedirs(app.root_path + "/static/uploads/products/{}".format(product_name))
                    except:
                        os.makedirs(app.root_path + "/static/uploads/products/{}".format(product_name))
                    filename = secure_filename(file.filename)
                    dir = app.root_path + "/static/uploads/products/{}".format(product_name)
                    file.save(os.path.join(dir, filename))
                    category = request.form['categories']
                    description = form.description.data.lower()
                    price = form.price.data
                    discount = form.discount.data
                    quantity = form.quantity.data

                    if discount != '' and discount != ' ':
                        p = round((float(price) * float(discount)) / 100, 2)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        cur.execute("UPDATE categories SET number_of_products = number_of_products + 1 WHERE category = %s", [category])
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published successfully!', 'success')
                        return redirect(url_for('admin_dashboard'))

                    if discount == "" or discount == " ":
                        p = 0
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        cur.execute("UPDATE categories SET number_of_products = number_of_products + 1 WHERE category = %s", [category])
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published successfully!', 'success')
                        return redirect(url_for('admin_dashboard'))

    elif result == 0:
        cur.close()
        flash('Create an category first to add a new product', 'warning')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_add_production.html', form=form, categories=categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)
                                
                # cur = mysql.connection.cursor()
                # cur.execute("INSERT INTO products(category, product_name, description, price, discount, files)\
                #              VALUES(%s, %s, %s, %s, %s, %s)", \
                #             (category, product_name, description, price, p, filename))
                # mysql.connection.commit()
                # cur.close()
                # flash('Your Product is published successfully!', 'success')
                # return redirect(url_for('admin_dashboard'))
    # return render_template('admin_add_production.html', form=form, categories=categories)


# admin edit product page

@app.route('/admin/edit_product/<id>', methods=['post', 'get'])
@is_admin_logged_in
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id={}".format(id))
    product = cur.fetchone()

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
    form = AddProductForm(request.form)
    form.product_name.data = product['product_name']
    form.description.data = product['description']
    form.price.data = product['price']
    form.quantity.data= product['quantity']
    # form.discount.data = product['discount']
    
    
    d = round((float(product['discount']) * float(100))/float(form.price.data), 2)
    form.discount.data = d
    
    
    if request.method == 'POST' and form.validate():
        product_name = request.form['product_name']

        folder = os.path.exists(app.root_path + "/static/uploads/products/{}".format(product_name))
        if folder == True and form.product_name.data == product_name:
            pass
        elif folder == False and form.product_name.data != product_name:
            pass
        else:
            flash('Folder Name Already Exists', 'warning')
            return redirect(request.url)

        file = request.files['file']
        if file and allowed_file(file.filename):
            rmtree(app.root_path + "/static/uploads/products/{}".format(product['product_name']))
            os.makedirs(app.root_path + "/static/uploads/products/{}".format(product_name))
            filename = secure_filename(file.filename)
            dir = app.root_path + "/static/uploads/products/{}".format(product_name)
            file.save(os.path.join(dir, filename))
        
            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, filename, id))
                mysql.connection.commit()
                cur.close()
                flash('Your Product Has been Edited successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            p = round((float(price) * float(discount)) / 100, 2)
            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, filename, id))
            mysql.connection.commit()
            cur.close()
            flash('Your Product Has been Edited successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        elif file.filename == '' or 'file' not in request.files:
            os.rename(os.path.join(app.root_path + "/static/uploads/products/{}".format(product['product_name'])),
                      os.path.join(app.root_path + "/static/uploads/products/{}".format(product_name)))
            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                             discount=%s, quantity=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, id))
                mysql.connection.commit()
                cur.close()
                flash('Your Product Has been Edited successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            p = round((float(price) * float(discount)) / 100, 2)
            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, id))
            mysql.connection.commit()
            cur.close()
            flash('Your Product Has been Edited successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_production.html', form=form, categories=categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin delete product

@app.route('/admin/delete_product/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, category FROM products WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['product_name']
    category = name['category']
    try:
        rmtree(app.root_path + "/static/uploads/products/{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM products WHERE id = %s", [id])
    cur.execute("DELETE FROM orders WHERE product_id = %s", [id])
    cur.execute("DELETE FROM reviews WHERE product_id = %s", [id])
    cur.execute("UPDATE categories SET number_of_products = number_of_products - 1 WHERE category = %s", [category])
    mysql.connection.commit()
    cur.close()
    flash('Your Product Has been Deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all products

@app.route('/admin/delete_all_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + "/static/uploads/products")
        flash('You Has been Deleted All Products successfully!', 'success')
    except:
        flash('You Has been Already Deleted All Products successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete product review

@app.route('/admin/delete_review_products/<id>/<id2>', methods=['post', 'get'])
@is_admin_logged_in
def delete_review_products(id, id2):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reviews WHERE product_id = %s AND id = %s", [id, id2])
    mysql.connection.commit()
    cur.execute("SELECT SUM(rate) / COUNT(product_id) AS total_avg_rate FROM reviews WHERE product_id = %s", [id])
    total = cur.fetchone()
    total_rate = total['total_avg_rate']
    cur.execute("UPDATE products SET avg_rate = %s WHERE id = %s", [total_rate, id])
    mysql.connection.commit()
    cur.close()
    flash('Product review has been deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all products reviews

@app.route('/admin/delete_all_review_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_review_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE reviews")
    cur.execute("UPDATE products SET avg_rate = '' ")
    mysql.connection.commit()
    cur.close()
    flash('All products reviews has been deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# slider product validators form

class AddProductsliderForm(Form):
    product_name = StringField('Name Of Product', [validators.InputRequired(), validators.length(min=1, max=180)])
    description = TextAreaField('Description', [validators.InputRequired()])
    price = IntegerField('Price', [validators.InputRequired()])
    discount = StringField('Discount Percentage %')
    quantity = StringField('Quantity', [validators.InputRequired()])
    # files = FileField('Add picture to Your Product', [validators.InputRequired()])


# admin add new slider product page

@app.route('/admin/add_product_slider', methods=['post', 'get'])
@is_admin_logged_in
def add_product_slider():
    form = AddProductsliderForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()

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
    if result > 0:
        if request.method == 'POST' and form.validate():
            product_name = form.product_name.data

            folder = os.path.exists(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
            if folder == True :
                flash('Folder Name Already Exists', 'warning')
                return redirect(url_for('add_product_slider'))
            cur = mysql.connection.cursor()
            cur.execute("SELECT product_name FROM slider_products WHERE product_name = BINARY %s", [product_name])
            res = cur.fetchone()
            if product_name in str(res):
                msg = "Product Name Already Exists"
                return render_template('admin_add_production_slider.html', form=form, msg=msg)
            slider_result = cur.execute("SELECT * FROM slider_products")
            if slider_result < 3:

                file = request.files['file']
                if file.filename == '':
                    flash('You Have to Select a File!', 'warning')
                if file and allowed_file(file.filename):
                    try:
                        rmtree(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
                        os.makedirs(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
                    except:
                        os.makedirs(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
                    filename = secure_filename(file.filename)
                    dir = app.root_path + "/static/uploads/slider_products/{}".format(product_name)
                    file.save(os.path.join(dir, filename))
                    category = request.form['categories']
                    description = form.description.data.lower()
                    price = form.price.data
                    discount = form.discount.data
                    quantity = form.quantity.data

                    if discount != '' and discount != ' ':
                        p = round((float(price) * float(discount)) / 100, 2)
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO slider_products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published to the slider uccessfully!', 'success')
                        return redirect(url_for('admin_dashboard'))

                    if discount == "" or discount == " ":
                        p = 0
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO slider_products(category, product_name, description, price, discount, quantity, files)\
                                                     VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                                    (category, product_name, description, price, p, quantity, filename))
                        mysql.connection.commit()
                        cur.close()
                        flash('Your Product is published to the slider successfully!', 'success')
                        return redirect(url_for('admin_dashboard'))
            else:
                flash('You can not add more 3 products in the slider!', 'warning')
                return redirect(url_for('admin_dashboard'))
    elif result == 0:
        flash('Create an category first to add new slider product', 'warning')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_production_slider.html', form=form, categories=categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin edit slider product page

@app.route('/admin/edit_product_slider/<id>', methods=['post', 'get'])
@is_admin_logged_in
def edit_product_slider(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT category FROM categories")
    categories = cur.fetchall()

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

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products WHERE id={}".format(id))
    product = cur.fetchone()
    cur.close()
    form = AddProductForm(request.form)
    form.product_name.data = product['product_name']
    form.description.data = product['description']
    form.price.data = product['price']
    form.quantity.data = product['quantity']
    # form.discount.data = product['discount']

    d = round((float(product['discount']) * float(100)) / float(form.price.data), 2)
    form.discount.data = d

    if request.method == 'POST' and form.validate():
        product_name = request.form['product_name']


        folder = os.path.exists(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
        if folder is True and form.product_name.data == product_name:
            pass
        elif folder is False and form.product_name.data != product_name:
            pass
        else:
            flash('Folder Name Already Exists', 'warning')
            return redirect(request.url)


        file = request.files['file']
        if file and allowed_file(file.filename):
            rmtree(app.root_path + "/static/uploads/slider_products/{}".format(product['product_name']))
            os.makedirs(app.root_path + "/static/uploads/slider_products/{}".format(product_name))
            filename = secure_filename(file.filename)
            dir = app.root_path + "/static/uploads/slider_products/{}".format(product_name)
            file.save(os.path.join(dir, filename))

            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE slider_products SET category=%s, product_name=%s, description=%s, price=%s,\
                             discount=%s, quantity=%s, files=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, filename, id))
                mysql.connection.commit()
                cur.close()
                flash('Your slider Product Has been Edited successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            p = round((float(price) * float(discount)) / 100, 2)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE slider_products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s, files=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, filename, id))
            mysql.connection.commit()
            cur.close()
            flash('Your slider Product Has been Edited successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        elif file.filename == '' or 'file' not in request.files:
            os.rename(os.path.join(app.root_path + "/static/uploads/slider_products/{}".format(product['product_name'])),
                      os.path.join(app.root_path + "/static/uploads/slider_products/{}".format(product_name)))
            category = request.form['categories']
            description = request.form['description']
            price = request.form['price']
            discount = request.form['discount']
            quantity = request.form['quantity']

            if discount == "" or discount == " ":
                p = 0
                cur = mysql.connection.cursor()
                cur.execute("UPDATE slider_products SET category=%s, product_name=%s, description=%s, price=%s,\
                             discount=%s, quantity=%s WHERE id=%s", \
                            (category, product_name, description, price, p, quantity, id))
                mysql.connection.commit()
                cur.close()
                flash('Your slider Product Has been Edited successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            p = round((float(price) * float(discount)) / 100, 2)
            
            
            cur = mysql.connection.cursor()
            cur.execute("UPDATE slider_products SET category=%s, product_name=%s, description=%s, price=%s,\
                         discount=%s, quantity=%s WHERE id=%s", \
                        (category, product_name, description, price, p, quantity, id))
            mysql.connection.commit()
            cur.close()
            flash('Your slider Product Has been Edited successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_production_slider.html', form=form, categories=categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin delete slider product

@app.route('/admin/delete_product_slider/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_product_slider(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name FROM slider_products WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['product_name']
    try:
        rmtree(app.root_path + "/static/uploads/slider_products/{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM slider_products WHERE id = %s", [id])
    cur.execute("DELETE FROM slider_reviews WHERE product_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Your slider Product Has been Deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all slider products

@app.route('/admin/delete_all_slider_products', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_slider_products():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + "/static/uploads/slider_products")
        flash('You Has been Deleted All slider Products successfully!', 'success')
    except:
        flash('You Has been Already Deleted All slider Products successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete slider product review

@app.route('/admin/delete_review_slider_product/<id>/<id2>', methods=['post', 'get'])
@is_admin_logged_in
def delete_review_slider_product(id, id2):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM slider_reviews WHERE product_id = %s AND id = %s", [id, id2])
    mysql.connection.commit()
    cur.execute("SELECT SUM(rate) / COUNT(product_id) AS total_avg_rate FROM slider_reviews WHERE product_id = %s", [id])
    total = cur.fetchone()
    total_rate = total['total_avg_rate']
    cur.execute("UPDATE slider_products SET avg_rate = %s WHERE id = %s", [total_rate, id])
    mysql.connection.commit()
    cur.close()
    flash('Slider product review has been deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all products reviews

@app.route('/admin/delete_all_slider_products_reviews', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_slider_products_reviews():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE slider_reviews")
    cur.execute("UPDATE slider_products SET avg_rate = '' ")
    mysql.connection.commit()
    cur.close()
    flash('All slider products reviews has been deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin create user account validator form

class AdduserForm(Form):
    first_name = StringField('First Name', [validators.InputRequired()])
    last_name = StringField('Last Name', [validators.InputRequired()])
    username = StringField('User Name', [validators.InputRequired()])
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords Do Not Match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# admin create user account page

@app.route('/admin/add_user', methods=['post', 'get'])
@is_admin_logged_in
def add_user():
    cur = mysql.connection.cursor()
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
    form = AdduserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data

        folder = os.path.exists(app.root_path + "/static/uploads/users/{}".format(username))
        if folder == True:
            flash('Folder Name Already Exists', 'warning')
            return redirect(url_for('add_user'))


        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", [username])
        res = cur.fetchone()
        cur.close()
        if username in str(res):
            msg = "User Name Already Exists"
            return render_template('admin_add_user.html', form=form, msg=msg, admin_name=session['admin_username'], admin_image=session['admin_image'])
        else:
            permission = request.form['permissions']
            first_name = form.first_name.data.lower()
            last_name = form.last_name.data.lower()
            email = request.form['email'].lower()
            gender = request.form['gender']
            country = request.form['country']
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))
            file = request.files['file']
            # if file.filename == '':
            #     flash('You Have to Select a File!', 'warning')
            try:
                rmtree(app.root_path + "/static/uploads/users/{}".format(username))
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
            except:
                os.makedirs(app.root_path + "/static/uploads/users/{}".format(username))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                dir = app.root_path + "/static/uploads/users/{}".format(username)
                file.save(os.path.join(dir, filename))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                             email, gender, country, username, password, reset_password_permission, files)\
                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (permission, first_name, last_name, email, gender,\
                             country, username, password, 'no_reset', filename))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created an Account successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            elif file.filename == '' or 'file' not in request.files:
                copy(app.root_path + '/static/admin.png', app.root_path + '/static/uploads/users/{}/admin.png'.format(username))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                                             email, gender, country, username, password, reset_password_permission, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (permission, first_name, last_name, email, gender, \
                             country, username, password, 'no_reset', 'admin.png'))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created an Account successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_user.html', form=form, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin delete user 

@app.route('/admin/delete_user/<id>', methods=['post', 'get'])
@is_admin_logged_in
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE id = %s", [id])
    name = cur.fetchone()
    n = name['username']
    try:
        rmtree(app.root_path + "/static/uploads/users/{}".format(n))
    except:
        pass
    cur.execute("DELETE FROM orders WHERE user_name = %s", [n])
    cur.execute("DELETE FROM buy_orders WHERE user_name = %s", [n])
    cur.execute("DELETE FROM reviews WHERE user_name = %s", [n])
    cur.execute("DELETE FROM slider_reviews WHERE user_name = %s", [n])
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('You Have Deleted User Account successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin add new category validator form

class CategoryForm(Form):
    category = StringField('Category', [validators.InputRequired(), validators.length(min=1, max=100)])
    

# admin add new category page

@app.route('/admin/add_category', methods=['post', 'get'])
@is_admin_logged_in
def add_category():
    cur = mysql.connection.cursor()

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
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        category = form.category.data.lower()
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM categories WHERE category = BINARY %s", [category])
        if result > 0:
            cur.close()
            flash('This Category Already Exists', 'warning')
            return redirect(url_for('admin_dashboard'))
        if category == ' ':
            cur.close()
            flash('You Should Type A Word!', 'warning')
            return redirect(url_for('add_category'))
        if result == 0:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO categories (category) VALUES(%s);", ([category]))
            mysql.connection.commit()
            cur.close()
            flash('You Have Added New Category successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_category.html', form=form, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin edit category page

@app.route('/admin/edit_category/<current_category>', methods=['post', 'get'])
@is_admin_logged_in
def edit_category(current_category):
        cur = mysql.connection.cursor()
        cur.execute("SELECT category FROM categories Where category=%s;", [current_category])
        cat = cur.fetchone()

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
        form = CategoryForm(request.form)
        form.category.data = cat['category']
        if request.method == 'POST' and form.validate():
            category = request.form['category'].lower()
            if category == ' ':
                cur.close()
                flash('You Should Type A Word!', 'warning')
                return redirect(url_for('add_category'))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE categories SET category=%s WHERE category=%s;", ([category], [current_category]))
            cur.execute("UPDATE products SET category=%s WHERE category=%s", \
                        ([category], [current_category]))
            cur.execute("UPDATE slider_products SET category=%s WHERE category=%s", \
                        ([category], [current_category]))
            mysql.connection.commit()
            cur.close()
            flash('You Have Edited Category successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_edit_category.html', form=form, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin delete category 

@app.route('/admin/delete_category/<category>', methods=['post', 'get'])
@is_admin_logged_in
def delete_category(category):
        cur = mysql.connection.cursor()
        prod = cur.execute("SELECT product_name FROM products WHERE category=%s", [category])
        if prod > 0:
            # flash('You Have products in This category', 'success')
            pass
        products = cur.fetchall()
        for product in products:
            rmtree(app.root_path + "/static/uploads/products/{}".format(product['product_name']))
            cur.execute("DELETE FROM reviews WHERE product_name=%s", [product['product_name']])
            mysql.connection.commit()

        slider = cur.execute("SELECT product_name FROM slider_products WHERE category=%s", [category])
        if slider > 0:
            pass
        sliders = cur.fetchall()
        for slider in sliders:
            rmtree(app.root_path + "/static/uploads/slider_products/{}".format(slider['product_name']))
            cur.execute("DELETE FROM slider_reviews WHERE product_name=%s", [slider['product_name']])
            mysql.connection.commit()

        cur.execute("DELETE FROM slider_products WHERE category=%s", [category])
        cur.execute("DELETE FROM products WHERE category=%s", [category])
        cur.execute("DELETE FROM categories Where category=%s;", [category])
        mysql.connection.commit()
        cur.close()        
        flash("You Have Deleted Category With it's products Successfully!", 'success')
        return redirect(url_for('admin_dashboard'))


# admin delete all categories

@app.route('/admin/delete_all_categories', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_categories():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE categories")
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE orders")
    cur.execute("TRUNCATE buy_orders")
    cur.execute("TRUNCATE reviews")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(app.root_path + "/static/uploads/products")
        rmtree(app.root_path + "/static/uploads/slider_products")
        flash('You Has been Deleted All Categories and Products Successfully!', 'success')
    except:
        flash('You Has been Deleted All Categories and Products Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all users

@app.route('/admin/delete_all_users', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_users():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT username FROM users WHERE permission = 'user'")
    if result >0:
        name = cur.fetchall()
        for n in name:
            rmtree(app.root_path + "/static/uploads/users/{}".format(n['username']))
    elif result == 0:
        pass
    cur.execute("DELETE FROM users WHERE permission = 'user' ")
    mysql.connection.commit()
    cur.close()
    flash('You Have Deleted All Users Account with their files successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin delete all accounts

@app.route('/admin/delete_all_accounts', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_accounts():
    try:
        rmtree(app.root_path + "/static/uploads/users")
        rmtree(app.root_path + "/static/uploads/products")
        rmtree(app.root_path + "/static/uploads/slider_products")
    except:
        pass
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE users")
    cur.execute("TRUNCATE categories")
    cur.execute("TRUNCATE products")
    cur.execute("TRUNCATE slider_products")
    cur.execute("TRUNCATE orders")
    cur.execute("TRUNCATE buy_orders")
    cur.execute("TRUNCATE reviews")
    cur.execute("TRUNCATE slider_reviews")
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('You Have Deleted All Accounts with their files successfully!', 'success')
    return redirect(url_for('admin_login'))


# admin accept orders

@app.route('/admin/accept_orders/<id>', methods=['post', 'get'])
@is_admin_logged_in
def accept_orders(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s", (['Accepted'], id))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted the order Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin accept all orders

@app.route('/admin/accept_all_orders', methods=['post', 'get'])
@is_admin_logged_in
def accept_all_orders():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s", (['Accepted']))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted all orders Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin reject orders

@app.route('/admin/reject_orders/<id>', methods=['post', 'get'])
@is_admin_logged_in
def reject_orders(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s", (['Rejected'], id))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected the order Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin reject all orders

@app.route('/admin/reject_all_orders', methods=['post', 'get'])
@is_admin_logged_in
def reject_all_orders():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s", (['Rejected']))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected all orders Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin search bar

@app.route('/search', methods=['GET', 'POST'])
@is_admin_logged_in
def search():
    if request.method == "POST":
        cur = mysql.connection.cursor()
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

        result = cur.execute("SELECT * FROM products \
                             WHERE( CONVERT(`product_name` USING utf8)\
                             LIKE %s)", [["%" + request.form['search'] + "%"]])
        search_products = cur.fetchall()
        cur.close()
        if result > 0:
            return render_template('admin_search.html', search_products=search_products, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)
        else:
            flash('No Products Found', 'warning')
            return redirect(url_for('admin_dashboard'))


# admin preview all slider products table page

@app.route('/admin/slider_products_table')
@is_admin_logged_in
def slider_products_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products")
    slider_products = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM slider_products")
    sliders = cur.fetchone()
    count_sliders = sliders['COUNT(id)']

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
    return render_template('admin_slider_products_table .html', slider_products=slider_products, count_sliders=count_sliders, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview all products table page

@app.route('/admin/products_table')
@is_admin_logged_in
def products_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

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
    return render_template('admin_products_table.html', products=products, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview all categories table page

@app.route('/admin/categories_table')
@is_admin_logged_in
def categories_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    cur.execute("SELECT COUNT(category) FROM categories")
    category = cur.fetchone()
    count_categories = category['COUNT(category)']
    cur.execute("SELECT COUNT(id) FROM products")
    products = cur.fetchone()
    count_products = products['COUNT(id)']

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
    return render_template('admin_categories_table.html', categories=categories, count_products=count_products, count_categories=count_categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# show all products in specific category

@app.route('/admin/categories/<category>', methods=['post', 'get'])
@is_admin_logged_in
def admin_categories(category):
    cur = mysql.connection.cursor()
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

    cur.execute("SELECT category, number_of_products FROM categories")
    all_categories = cur.fetchall()
    result = cur.execute("SELECT * FROM products WHERE category=%s", [category])
    categories = cur.fetchall()
    cur.close()
    if result > 0:
        return render_template('admin_catigories.html', category=category, categories=categories, all_categories=all_categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)
    else:
        msg = 'No Products Found!'
        return render_template('admin_catigories.html', msg=msg, category=category, all_categories=all_categories, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview all users table page

@app.route('/admin/users_table')
@is_admin_logged_in
def users_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.execute("SELECT COUNT(username) FROM users WHERE permission = 'user'")
    count_userss = cur.fetchone()
    count_users = count_userss['COUNT(username)']

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
    return render_template('admin_users_table.html', users=users, count_users=count_users, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview all users table page

@app.route('/admin/orders_table')
@is_admin_logged_in
def orders_table():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT SUM(quantity) AS QUANTITY , user_name AS USERNAME, SUM((price * quantity) - (quantity * discount)) AS TOTAL FROM buy_orders T GROUP BY user_id")
    cur.execute("SELECT * FROM buy_orders ;")
    orders = cur.fetchall()

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
    return render_template('admin_orders_table.html', orders=orders, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin review products table page

@app.route('/admin/review_products')
@is_admin_logged_in
def review_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reviews")
    review_products = cur.fetchall()

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
    return render_template('admin_products_reviews.html', review_products=review_products, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin review products table page

@app.route('/admin/review_slider_products')
@is_admin_logged_in
def review_slider_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_reviews")
    review_slider_products = cur.fetchall()

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
    return render_template('admin_slider_products_reviews.html', review_slider_products=review_slider_products, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview product

@app.route('/admin/product/<id>')
@is_admin_logged_in
def product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", [id])
    product = cur.fetchone()
    reviewresult = cur.execute("SELECT * FROM reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    review = cur.fetchone()
    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

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
    return render_template('admin_product.html', product=product, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], reviewresult=reviewresult, review=review, rate=rate, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin preview product

@app.route('/admin/slider/<id>')
@is_admin_logged_in
def slider(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM slider_products WHERE id = %s", [id])
    product = cur.fetchone()
    reviewresult = cur.execute("SELECT * FROM slider_reviews WHERE product_id={} ORDER BY id DESC limit 1".format(id))
    review = cur.fetchone()
    cur.execute("SELECT SUM(rate) / COUNT(product_name) AS avg_rate FROM slider_reviews WHERE product_id = %s;", [id])
    rate = cur.fetchone()

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
    return render_template('admin_slider.html', product=product, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], reviewresult=reviewresult, review=review, rate=rate, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# view messages table page

@app.route('/admin/messages_table', methods=['post', 'get'])
@is_admin_logged_in
def admin_messages_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contact_us ;")
    all_messages = cur.fetchall()
    cur.execute("SELECT status FROM contact_us WHERE status = %s ;", ['seen'])
    seen_messages = cur.fetchall()
    cur.execute("SELECT status FROM contact_us WHERE status = %s ;", ['not_seen'])
    not_seen_messages = cur.fetchall()

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
    return render_template('admin_messages_table.html', admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], all_messages=all_messages, seen_messages=seen_messages, not_seen_messages=not_seen_messages, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# view message page

@app.route('/admin/message/<id>', methods=['post', 'get'])
@is_admin_logged_in
def admin_message(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contact_us WHERE id = %s ;", [id])
    current_message = cur.fetchone()
    cur.execute("UPDATE contact_us SET status = %s WHERE id = %s", (['seen'], id))
    mysql.connection.commit()

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
    return render_template('admin_message.html', admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], current_message=current_message, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# delete message

@app.route('/admin/delete_message/<id>', methods=['post', 'get'])
@is_admin_logged_in
def admin_delete_message(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_us WHERE id = %s ;", [id])
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted the message!', 'success')
    return redirect(url_for('admin_dashboard'))


# delete all messages

@app.route('/admin/delete_all_messages', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_messages():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE contact_us")
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted all messages!', 'success')
    return redirect(url_for('admin_dashboard'))


# delete all seen messages

@app.route('/admin/delete_all_seen_messages', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_seen_messages():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_us WHERE status = %s ", ['seen'])
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted all seen messages!', 'success')
    return redirect(url_for('admin_dashboard'))


# delete all not seen messages

@app.route('/admin/delete_all_not_seen_messages', methods=['post', 'get'])
@is_admin_logged_in
def delete_all_not_seen_messages():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contact_us WHERE status = %s ", ['not_seen'])
    mysql.connection.commit()
    cur.close()
    flash('You have successfully deleted all not seen messages!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin show orders details for user

@app.route('/admin/show_orders/<username>', methods=['post', 'get'])
@is_admin_logged_in
def show_orders(username):
    session['orders_username'] = username
    cur = mysql.connection.cursor()
    # cur.execute("SELECT SUM(quantity) AS QUANTITY , user_name AS USERNAME, SUM((price * quantity) - (quantity * discount)) AS TOTAL FROM buy_orders T GROUP BY user_id")
    cur.execute("SELECT * FROM buy_orders WHERE user_name = %s ;", [username])
    orders = cur.fetchall()

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
    return render_template('admin_show_orders_by_user_table.html', admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], orders=orders, messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)


# admin accept orders for user

@app.route('/admin/accept_order_user/<username>/<id>', methods=['post', 'get'])
@is_admin_logged_in
def accept_order_user(username, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s AND user_name = %s", (['Accepted'], id, username))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted the order Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin accept all orders for user

@app.route('/admin/accept_all_orders_user/<username>', methods=['post', 'get'])
@is_admin_logged_in
def accept_all_orders_user(username):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE user_name = %s ", (['Accepted'], username))
    mysql.connection.commit()
    cur.close()
    flash('You have accepted all orders Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin reject orders for user

@app.route('/admin/reject_order_user/<username>/<id>', methods=['post', 'get'])
@is_admin_logged_in
def reject_order_user(username, id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE id = %s AND user_name = %s", (['Rejected'], id, username))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected the order Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# admin reject all orders for user

@app.route('/admin/reject_all_orders_user/<username>', methods=['post', 'get'])
@is_admin_logged_in
def reject_all_orders_user(username):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE buy_orders SET status = %s WHERE user_name = %s", (['Rejected'], username))
    mysql.connection.commit()
    cur.close()
    flash('You have rejected all orders Successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# run whole application function

if __name__ == '__main__':
    app.secret_key = 'PGHhsV7MXGJlsFAiSq9Y5kngjUKJeKtSBjjdyjnr2gDa01irRsNC7ZNwg3NlsTIHv39N8iOsV6z87wG3d5CGBqIRAm29pWXM9czwVmkcH0qjvvIi7INPhTwCNoDelyute2ljQQXoYuonzUzcF9ToPD2gL0coxbrOhwMeaxZeFK7y4AtRgya27lSASLKjQf5bYRfZkjl1v7q9JvpJBwaGNuwK5fxOPsxciRp8Hf4PEmfeFXBkIYsKzIqGwE'
    app.run(debug=True)
