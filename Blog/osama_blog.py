# imports to make app work correctly

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging , send_from_directory, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail, Message
from shutil import rmtree
# from PIL import Image
# from io import BytesIO
# from flask.helpers import flash
import MySQLdb
import os
import random
import string
# import uuid
from werkzeug.utils import secure_filename
# from flask_uploads import UploadSet, configure_uploads, IMAGES


# connect to database in localhost to create database and their tables

database = MySQLdb.connect("localhost", "OSAMA", "OSAMA")
cursor = database.cursor()
# cursor.execute("DROP DATABASE IF EXISTS osama_blog;")
cursor.execute("CREATE DATABASE IF NOT EXISTS osama_blog DEFAULT CHARSET UTF8")
database.select_db('osama_blog')
# cursor.execute("DROP TABLE IF EXISTS users;")
# cursor.execute("DROP TABLE IF EXISTS articles;")
# cursor.execute("DROP TABLE IF EXISTS short_link;")
# cursor.execute("DROP TABLE IF EXISTS about_me;")

cursor.execute("CREATE TABLE IF NOT EXISTS users(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                name VARCHAR(100) NOT NULL,\
                email VARCHAR(100) NOT NULL,\
                username VARCHAR(100) NOT NULL,\
                password VARCHAR(100) NOT NULL,\
                files TEXT NOT NULL,\
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP );")

cursor.execute("CREATE TABLE IF NOT EXISTS articles(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                category VARCHAR(100) NOT NULL,\
                title VARCHAR(255) NOT NULL,\
                author VARCHAR(100) NOT NULL,\
                body TEXT NOT NULL,\
                files TEXT NOT NULL,\
                written_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute("CREATE TABLE IF NOT EXISTS short_link(\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                original_link varchar(255) UNIQUE NOT NULL,\
                short_link TEXT NOT NULL,\
                process_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP );")

cursor.execute("CREATE TABLE IF NOT EXISTS about_me(picture VARCHAR(100) PRIMARY KEY);")

database.close()


app = Flask(__name__)

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://OSAMA:OSAMA@localhost/osama_blog2'
db = SQLAlchemy(app)
admin = Admin(app)


# application configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'osama_blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# application configuration to send email with gmail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'osama.blog.py@gmail.com'
app.config['MAIL_PASSWORD'] = 'blogPYosama'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# website icon

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'i.ico', mimetype='image/vnd.microsoft.icon')


# home page 

@app.route('/')
def home_page():
    return render_template('home.html')


# url shortener form

@app.route('/result', methods=['GET', 'POST'])
def result():
    cur = mysql.connection.cursor()
    r = request.form['url']
    if r == None or r == "" or r == " ":
        return redirect(url_for('home_page'))
    cur.execute("SELECT original_link FROM short_link WHERE original_link=%s", [r])
    sl = cur.fetchone()
    if r in str(sl):
        cur.execute("SELECT * FROM short_link WHERE original_link=%s", [r])
        sl2 = cur.fetchone()
        return render_template('url_exists.html', sl2=sl2)
    else:
        # def random_string(string_length=5):
        #     return str(uuid.uuid4())[0:string_length]
        def random_string():
            return ("".join([random.choice(string.ascii_letters + string.digits) for i in range(6)]))
        cur.execute("INSERT INTO short_link(original_link, short_link)\
                             VALUES(%s, %s)", ([r], [random_string()]))
        mysql.connection.commit()
        res = cur.execute("SELECT * FROM short_link WHERE original_link=%s", [r])
        short_link = cur.fetchone()
        if res > 0:
            return render_template('url_result.html', short_link=short_link)
        else:
            msg = 'No Urls Found!'
            return render_template('url_fail.html', msg=msg, short_link=short_link)
    cur.close()
    return redirect(url_for('home_page'))


# redirect page

@app.route('/redirect/<url_name>')
# def href(url_name):
def redirect_link(url_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT short_link FROM short_link WHERE short_link=%s", [url_name])
    ff = cur.fetchone()
    if url_name in str(ff):
        cur.execute("SELECT original_link FROM short_link WHERE short_link=%s", [url_name])
        f = cur.fetchone()
        for i in f:
            return redirect(f[i])
    else:
        return render_template('url_redirect_fail.html')
    # return redirect(url_for(f.original_link))
    msg = 'No Urls Found!'
    cur.close()
    return render_template('url_redirect_fail.html', msg=msg)


# apout page

@app.route('/about')
def about():
    cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO about_me(picture)\
    #                              VALUES(%s)", ['about_me.png'])
    # mysql.connection.commit()
    cur.execute("SELECT picture FROM about_me")
    article = cur.fetchone()
    cur.close()
    return render_template('about.html', article=article)


# all articles page 

@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    cur.close()


# redirect to categories.html from articles page form

@app.route('/categories', methods=['post'])
def categories():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        if request.form['categories'] == request.form['categories']:
            result = cur.execute("SELECT * FROM articles WHERE category=%s", [request.form['categories']])
            articles = cur.fetchall()
            cur.close()
            if result > 0:
                # flash("done!", "success")
                return render_template('categories.html', articles=articles)
            else:
                # flash("done2!", "success")
                msg = 'No Articles Found'
                return render_template('categories.html', msg=msg)
        # elif request.form['categories'] == request.form['categories']:
        #     result = cur.execute("SELECT * FROM articles WHERE category=%s", [request.form['categories']])
        #     articles = cur.fetchall()
        #     cur.close()
        #     if result > 0:
        #         flash("done!", "success")
        #         return render_template('categories.html', articles=articles)
        #     else:
        #         flash("done2!", "success")
        #         msg = 'No Articles Found'
        #         return render_template('categories.html', msg=msg)
    return render_template('categories.html')


# search by category from dashboard page

@app.route('/search_by_categories/<category>', methods=['post', 'get'])
def category(category):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
                              WHERE(CONVERT(`category` USING utf8)\
                              LIKE %s)", ["%" + category + "%"])
        articles = cur.fetchall()
        cur.close()
        if result > 0:
            return render_template('categories.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('categories.html', msg=msg)


# display article picture from dashboard page

@app.route('/article_picture/<id>/<picture_name>', methods=['post', 'get'])
def article_picture(id, picture_name):
    return render_template('article_picture.html', id=id, picture_name=picture_name)


# display article picture from article page

@app.route('/article_picture_inner/<id>/<user_name>/<pic>', methods=['post', 'get'])
def article_picture_inner(id, user_name, pic):
    return render_template('article_picture_inner.html', id=id, user_name=user_name, pic=pic)


# display profile picture from dashboard page

@app.route('/profile_picture/<pic>', methods=['post', 'get'])
def profile_picture(pic):
    username = session['username']
    return render_template('profile_picture.html', pic=pic, username=username)


# show article page

# @app.route('/article/<string:id>/')
# def article(id):
#     if 'logged_in' in session:
#         user_name = session['username']
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM articles WHERE id = {}".format(id))
#         article = cur.fetchone()
#         return render_template('article.html', article=article, user_name=user_name, id=id)
#         cur.close()
#     else:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM articles WHERE id = {}".format(id))
#         article = cur.fetchone()
#         cur.execute("SELECT author FROM articles WHERE id = {}".format(id))
#         art = cur.fetchone()
#         for user in art:
#             session['author'] = art[user]
#             return render_template('article.html', article=article, user_name=art[user], id=id)
#     return render_template('article.html', article=article,  user_name=session['author'], id=id)

@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id = {}".format(id))
    article = cur.fetchone()
    cur.execute("SELECT author FROM articles WHERE id = {}".format(id))
    art = cur.fetchone()
    for user in art:
        return render_template('article.html', article=article, user_name=art[user], id=id)


# register form validators 

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Email("Field must be a valid email address.")])
    username = StringField('Username', [validators.Length(min=6, max=100)])
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords Do Not Match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# register page

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data.lower()
        email = form.email.data.lower()
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = BINARY %s", [username])
        res = cur.fetchone()
        if username in str(res):
            msg = "Username Already Exists"
            return render_template('register.html', form=form, msg=msg)
        else:
            cur.execute("INSERT INTO users(name, email, username, password)\
                         VALUES(%s, %s, %s, %s)", (name, email, username, password))
            mysql.connection.commit()
            cur.close()
            flash('You Are Now Registered And You Can login!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


# login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        # collate utf8_bin
        result = cur.execute("SELECT * FROM users WHERE username = BINARY %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['register_date'] = data['register_date']
                flash('Now You Are Logged In ', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Wrong Password!'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username Can Not Be Found!'
            return render_template('login.html', error=error)
    return render_template('login.html')


# check if user is still logged in 

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session :
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap


# log out

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You Are Now Logged Out', 'success')
    return redirect(url_for('login'))


# dashboard page

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    username = session['username']
    result = cur.execute("SELECT * FROM articles WHERE author=%s", [username])
    articles = cur.fetchall()
    cur.execute("SELECT files FROM users WHERE username=%s", [username])
    art = cur.fetchone()
    if result > 0:
        return render_template('dashboard.html', articles=articles, username=username, art=art)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg, username=username, art=art)
    cur.close()


# add new article validators

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=10)])


# add new article page

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(category, title, body, author) \
                     VALUES(%s, %s, %s, %s)", ([request.form['categories']], title, body, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Article Has Been Created Successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)


# edit article page

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    session['edit_article_id'] = id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    cur.close()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur = mysql.connection.cursor()
        app.logger.info(title)
        cur.execute("UPDATE articles SET category=%s, title=%s, body=%s WHERE id=%s", ([request.form['categories']], title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Article Has Been Updated Successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)


# delete article

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles\article{}".format(session['username'], id))
        flash('Article Has Been Deleted Successfully', 'success')
    except:
        flash('Article Has Been Deleted Successfully', 'success')
    return redirect(url_for('dashboard'))


# delete all articles
@app.route('/delete_all_articles', methods=['POST'])
@is_logged_in
def delete_all_articles():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE author = %s", [session['username']])
    mysql.connection.commit()
    cur.close()
    try:
        rmtree(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles".format(session['username']))
        flash('All Articles Has Been Deleted Successfully', 'success')
    except:
        flash('All Articles Has Been Already Deleted Successfully', 'success')
    return redirect(url_for('dashboard'))


# delete account and articles

@app.route('/delete_account', methods=['POST'])
@is_logged_in
def delete_account():
    cur = mysql.connection.cursor()
    username = session['username']
    cur.execute("DELETE FROM users WHERE username = %s", [username])
    cur.execute("DELETE FROM articles WHERE author = %s", [username])
    mysql.connection.commit()
    cur.close()
    try:
        dir = r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}".format(session['username'])
        rmtree(dir)
        session.clear()
        flash('Your Account Has Been Deleted Successfully', 'success')
    except:
        session.clear()
        flash('Your Account Has Been Deleted Successfully', 'success')
    return render_template('home.html')


# upload terms

# UPLOAD_FOLDER = r'C:\Users\OSAMA\Desktop\final\uploads'
UPLOAD_FOLDER = r'C:\Users\OSAMA\Desktop\final\static\uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# check if file is in allowed extensions

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload_file_locally', methods=['GET', 'POST'])
# @is_logged_in
# def upload_file_locally():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'warning')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'warning')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             session['upload_file_locally'] = filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             flash('Your File Has been uploaded Successfully', 'success')
#             return redirect(url_for('download'))
#             # return redirect(url_for('dashboard'))
#             # return redirect(url_for('dashboard', filename=filename))
#         else:
#             flash('Not allowed file', 'warning')
#             return redirect(request.url)
#     return render_template('upload_locally.html')


# upload file locally and in database together -- profile picture --

@app.route('/upload_file_locally', methods=['GET', 'POST'])
@is_logged_in
def upload_file_locally():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File Part', 'warning')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Your File Has Been Uploaded Successfully', 'success')
            sor = "{}\{}".format(UPLOAD_FOLDER, filename)
            flash(sor, 'success')
            # flash("{}\{}".format(UPLOAD_FOLDER, filename), 'success')
            # cur = mysql.connection.cursor()
            # cur.execute("UPDATE users SET files=%s WHERE username=%s", (sor, session['username']))
            # mysql.connection.commit()
            # cur.close()
            return redirect(url_for('dashboard'))
            # return redirect(request.url)
        else:
            flash('Not Allowed File', 'warning')
            return redirect(request.url)
    return render_template('upload_locally.html')


# upload file to database -- profile picture --

@app.route('/upload', methods=['GET', 'POST'])
@is_logged_in
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File Part!', 'warning')
            return redirect(url_for('dashboard'))
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File!', 'warning')
            return redirect(url_for('dashboard'))
        try:
            rmtree(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\profile_picture".format(session['username']))
            os.makedirs(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\profile_picture".format(session['username']))
        except:
            os.makedirs(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\profile_picture".format(session['username']))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dir = r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\profile_picture".format(session['username'])
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET files=%s WHERE username=%s", (filename, session['username']))
            mysql.connection.commit()
            cur.close()
            flash('Your File Has Been Uploaded Successfully!', 'success')
            return redirect(url_for('dashboard'))
            # return redirect(url_for('upload_file', filename=filename))
        else:
            flash('Not Allowed File!', 'warning')
            return redirect(url_for('dashboard'))
    return render_template('upload.html')



# @app.route('/upload', methods=['GET', 'POST'])
# @is_logged_in
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'warning')
#             return redirect(url_for('dashboard'))
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'warning')
#             return redirect(url_for('dashboard'))
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             cur = mysql.connection.cursor()
#             cur.execute("UPDATE users SET files=%s WHERE username=%s", (filename, session['username']))
#             mysql.connection.commit()
#             cur.close()
#             flash('Your File Has been uploaded Successfully', 'success')
#             return redirect(url_for('dashboard'))
#             # return redirect(url_for('upload_file', filename=filename))
#         else:
#             flash('Not allowed file', 'warning')
#             return redirect(url_for('dashboard'))
#     return render_template('upload.html')


# upload file to database -- article picture --

@app.route('/upload_file_article', methods=['GET', 'POST'])
@is_logged_in
def upload_file_article():
    id = session['edit_article_id']
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File Part!', 'warning')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File!', 'warning')
            return redirect(request.url)
        try:
            rmtree(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles\article{}".format(session['username'], id))
            os.makedirs(r"static\uploads\users\{}\articles\article{}".format(session['username'], id))
        except:
            os.makedirs(r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles\article{}".format(session['username'], id))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dir = r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles\article{}".format(session['username'], id)
            file.save(os.path.join(dir, filename))
            cur = mysql.connection.cursor()
            cur.execute("UPDATE articles SET files=%s WHERE id=%s", (filename, id))
            mysql.connection.commit()
            cur.close()
            flash('Article File Has Been Uploaded Successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Not Allowed File!', 'warning')
            return redirect(request.url)
    return redirect(url_for('dashboard'))



# @app.route('/upload_file_article', methods=['GET', 'POST'])
# @is_logged_in
# def upload_file_article():
#     id = session['edit_article_id']
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             cur = mysql.connection.cursor()
#             cur.execute("UPDATE articles SET files=%s WHERE id=%s", (filename, id))
#             mysql.connection.commit()
#             cur.close()
#             flash('Article File Has been uploaded Successfully', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Not allowed file', 'warning')
#             return redirect(request.url)
#     return redirect(url_for('dashboard'))


# delete profile file from database 

@app.route('/delete_file', methods=['POST'])
@is_logged_in
def delete_file():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET files='' WHERE username=%s", [session['username']])
    mysql.connection.commit()
    cur.close()
    dir = r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\profile_picture".format(session['username'])
    try:
        rmtree(dir)
        flash('Your File Has Been Deleted Successfully!', 'success')
    except:
        flash('Your File Has Been Already Deleted Before!', 'warning')
    # os.remove(os.path.join(dir))
    # os.unlink(os.path.join(dir))
    return redirect(url_for('dashboard'))


# delete article file from database

@app.route('/delete_article_file', methods=['POST'])
@is_logged_in
def delete_article_file():
    id = session['edit_article_id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE articles SET files='' WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    dir = r"C:\Users\OSAMA\Desktop\final\static\uploads\users\{}\articles\article{}".format(session['username'], id)
    try:
        rmtree(dir)
        flash('Article File Has Been Deleted Successfully!', 'success')
    except:
        flash('Article File Has Been Already Deleted Before!', 'warning')
    # flash('Article File Have Been Deleted Successfully', 'success')
    return redirect(url_for('dashboard'))


# general search bar in navbar

@app.route('/search', methods=['GET', 'POST'])
@is_logged_in
def search():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                          WHERE(CONVERT(`author` USING utf8)\
        #                          LIKE %s)" , [request.form['search']])
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                                  WHERE( CONVERT(`author` USING utf8)\
        #                                  LIKE %s )", ["%" + request.form['search'] + "%"])
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                                          WHERE( CONVERT(`author` USING utf8)\
        #                                          LIKE %s OR CONVERT(`title` USING utf8)\
        #                                          LIKE %s)", [["%" + request.form['search'] + "%"], ["%" + request.form['search'] + "%"]])
        result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
                                                 WHERE( CONVERT(`author` USING utf8)\
                                                 LIKE %s OR CONVERT(`title` USING utf8)\
                                                 LIKE %s OR CONVERT(`id` USING utf8)\
                                                 LIKE %s)", [["%" + request.form['search'] + "%"],\
                                                            ["%" + request.form['search'] + "%"], \
                                                            ["%" + request.form['search'] + "%"]])
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                       WHERE(CONVERT(`author` USING utf8)\
        #                       LIKE %s)", [request.form['search'] + "%"])
        articles = cur.fetchall()
        cur.close()
        if result > 0:
            # flash("done!", "success")
            return render_template('search.html', articles=articles)
        else:
            # flash("done2!", "success")
            msg = 'No Articles Found'
            return render_template('search.html', msg=msg)
        # return redirect(url_for('home_page'))
    # flash("done3!", "success")
    return render_template('search.html')


# searches page

@app.route('/searches', methods=['GET', 'POST'])
@is_logged_in
def searches():
    return render_template('searches.html')


# search in authors only

@app.route('/search_author', methods=['GET', 'POST'])
@is_logged_in
def search_author():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                          WHERE(CONVERT(`author` USING utf8)\
        #                          LIKE %s)" , [request.form['search']])
        result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
                                         WHERE(CONVERT(`author` USING utf8)\
                                         LIKE %s)", ["%" + request.form['search'] + "%"])
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                       WHERE(CONVERT(`author` USING utf8)\
        #                       LIKE %s)", [request.form['search'] + "%"])
        articles = cur.fetchall()
        cur.close()
        if result > 0:
            # flash("done!", "success")
            return render_template('search_author.html', articles=articles)
        else:
            # flash("done2!", "success")
            msg = 'No Authors Found'
            return render_template('search_author.html', msg=msg)
        # return redirect(url_for('home_page'))
    # flash("done3!", "success")
    return render_template('search_author.html')


# search in title only

@app.route('/search_title', methods=['GET', 'POST'])
@is_logged_in
def search_title():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                          WHERE(CONVERT(`author` USING utf8)\
        #                          LIKE %s)" , [request.form['search']])
        result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
                                         WHERE(CONVERT(`title` USING utf8)\
                                         LIKE %s)", ["%" + request.form['search'] + "%"])
        # result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
        #                       WHERE(CONVERT(`author` USING utf8)\
        #                       LIKE %s)", [request.form['search'] + "%"])
        articles = cur.fetchall()
        cur.close()
        if result > 0:
            # flash("done!", "success")
            return render_template('search_title.html', articles=articles)
        else:
            # flash("done2!", "success")
            msg = 'No Titles Found'
            return render_template('search_title.html', msg=msg)
        # return redirect(url_for('home_page'))
    # flash("done3!", "success")
    return render_template('search_title.html')


# dropdown search in Author and Title

@app.route('/search_drop_down', methods=['GET', 'POST'])
@is_logged_in
def search_drop_down():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        if request.form['search_type'] == 'author':
            if request.form['search'] == 'search' or request.form['search'] == '' or request.form['search'] == ' ':
                flash("You have not written anything to search for !", "warning")
                return redirect(url_for('searches'))
            result = cur.execute("SELECT * FROM articles WHERE author = %s", [request.form['search']])
            articles = cur.fetchall()
            cur.close()
            if result > 0:
                # flash("done!", "success")
                return render_template('search_drop_down.html', articles=articles)
            else:
                # flash("done2!", "success")
                msg = 'No Authors Found'
                return render_template('search_drop_down.html', msg=msg)
        elif request.form['search_type'] == 'title':
            if request.form['search'] == 'search' or request.form['search'] == '' or request.form['search'] == ' ':
                flash("You have not written anything to search for !", "warning")
                return redirect(url_for('searches'))
            result = cur.execute("SELECT * FROM articles WHERE title = %s", [request.form['search']])
            articles = cur.fetchall()
            cur.close()
            if result > 0:
                # flash("done!", "success")
                return render_template('search_drop_down.html', articles=articles)
            else:
                # flash("done2!", "success")
                msg = 'No Articles Found'
                return render_template('search_drop_down.html', msg=msg)
    return redirect(url_for('searches'))


# forget password page
# redirect to forget_password.html

@app.route("/forget_password")
def forget_password():
    return render_template('forget_password.html')


# send email with the whole account information

@app.route("/account_information", methods=['GET', 'POST'])
def account_information():
    if request.form['email'] == '':
        flash('You did not write an email !', 'warning')
        return redirect(url_for('home_page'))
    em = request.form['email']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT * FROM users WHERE email = %s", [em])
    res = cur.fetchone()
    if r > 0:
        msg = Message()
        msg.sender = 'osama.blog.py@gmail.com'
        msg.subject = "Account Information"
        msg.recipients = [em]
        msg.body = " Your id is : %s \n Your name is : %s \n Your username is : %s \n Your password is : %s \n Your email is : %s \n Your registeration date is : %s \n message sent from Flask-Mail Automatic sender!" % (res['id'], res['name'], res['username'], res['password'], res['email'], res['register_date'])
        mail.send(msg)
        flash("The Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('home_page'))
    else:
        flash("This email Not Found!", "warning")
        return redirect(url_for('home_page'))


# send email with the link to reset password >> reset/id

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.form['email'] == '':
        flash('You did not write an email !', 'warning')
        return redirect(url_for('home_page'))
    em = request.form['email']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT id, email FROM users WHERE email = %s", [em])
    res = cur.fetchone()
    if r > 0:
        msg = Message()
        msg.sender = 'osama.blog.py@gmail.com'
        msg.subject = "Reset Your Password"
        msg.recipients = [em]
        msg.body = "Reset Your Password : http://localhost:5000/reset/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'])
        mail.send(msg)
        flash("The Reset Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('home_page'))
    else:
        flash("This email Not Found!", "warning")
        return redirect(url_for('home_page'))


# redirect to reset.html >>> to show the reset form with encryption

@app.route("/reset/<id>", methods=['GET', 'POST'])
def reset(id):
    session['reset_password_id'] = id
    return render_template('reset.html', id=id)


# redirect from reset.html >>> to insert new password with encryption into database

@app.route("/reset_password2", methods=['POST'])
def reset_password2():
    # p = request.form['password']
    rp = sha256_crypt.encrypt(str(request.form['password']))
    id = session['reset_password_id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET password = %s WHERE id = %s", [rp, id])
    mysql.connection.commit()
    cur.close()
    flash("You Have Successfully Changed Your Password, You Can Login Now!", "success")
    return redirect(url_for('home_page'))


# redirect to forget_password.html
# send email with the link to reset password >> reset_pass/id

@app.route("/reset_passe", methods=['GET', 'POST'])
def reset_passe():
    if request.form['email'] == '':
        flash('You did not write an email !', 'warning')
        return redirect(url_for('home_page'))
    em = request.form['email']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT id, email FROM users WHERE email = %s", [em])
    res = cur.fetchone()
    if r > 0:
        msg = Message()
        msg.sender = 'osama.blog.py@gmail.com'
        msg.subject = "Reset Your Password"
        msg.recipients = [em]
        msg.body = "Reset Your Password : http://localhost:5000/reset_pass/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'])
        mail.send(msg)
        flash("The Reset Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('home_page'))
    else:
        flash("This email Not Found!", "warning")
        return redirect(url_for('home_page'))


# reset password form validators
# put validators to data in encrypted reset form

class reset_password(Form):
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# redirect from reset2.html >>> to insert new password with encryption into database

@app.route("/reset_pass/<id>", methods=['GET', 'POST'])
def reset_pass(id):
    form = reset_password(request.form)
    if request.method == 'POST' and form.validate():
        rp = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE id = %s", [rp, id])
        mysql.connection.commit()
        cur.close()
        flash("You Have Successfully Changed Your Password Now!", "success")
        return redirect(url_for('home_page'))
    return render_template('reset2.html', form=form)


# redirect to forget_password.html
# send email with the link to reset password >> reset_pass_user/id

@app.route("/reset_passu", methods=['GET', 'POST'])
def reset_passu():
    if request.form['text'] == '':
        flash('You did not write a username !', 'warning')
        return redirect(url_for('home_page'))
    un = request.form['text']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT id, email, username FROM users WHERE username = %s", [un])
    res = cur.fetchone()
    if r > 0:
        emm = res['email']
        msg = Message()
        msg.sender = 'osama.blog.py@gmail.com'
        msg.subject = "Reset Your Password"
        msg.recipients = [emm]
        msg.body = "Reset Your Password : http://localhost:5000/reset_pass_user/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'])
        mail.send(msg)
        flash("The Reset Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('home_page'))
    else:
        flash("This email Not Found!", "warning")
        return redirect(url_for('home_page'))


# reset password form validators
# put validators to data in encrypted reset form

class reset_passwordu(Form):
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])


# redirect from reset3.html >>> to insert new password with encryption into database

@app.route("/reset_pass_user/<id>", methods=['GET', 'POST'])
def reset_pass_user(id):
    form = reset_passwordu(request.form)
    if request.method == 'POST' and form.validate():
        rp = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE id = %s", [rp, id])
        mysql.connection.commit()
        cur.close()
        flash("You Have Successfully Changed Your Password Now!", "success")
        return redirect(url_for('home_page'))
    return render_template('reset3.html', form=form)


# run whole application function

if __name__ == '__main__' :
    app.secret_key = 'osama_blog'
    app.run(debug=True)




# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == "POST":
#         cur = mysql.connection.cursor()
#         # result = cur.execute("SELECT * FROM articles")
#         # result = cur.execute("SELECT * FROM articles\
#         #                       WHERE author = %s", [session['username']])
#         # result = cur.execute("SELECT * FROM articles\
#         #                       WHERE author = %s", ["OSAMA.MOHAMED"])
#         # result = cur.execute("SELECT * FROM articles\
#         #                       WHERE author = %s", ["searchbarr"])
#         # result = cur.execute("SELECT * FROM articles\
#         #                       WHERE author = %s", [request.form['search']])
#         articles = cur.fetchall()
#         cur.close()
#         if result > 0:
#             flash("done!", "success")
#             return render_template('search.html', articles= articles)
#         else:
#             flash("done2!", "success")
#             msg = 'No Articles Found'
#             return render_template('search.html', msg=msg)
#         # return redirect(url_for('home_page'))
#     flash("done3!", "success")
#     return render_template('search.html')





# @app.route('/download', methods=['get'])
# def download():
#     # return "{}/{}".format(UPLOAD_FOLDER, session['upload_file_locally'])#
#     return send_file(BytesIO({{{{{{{{fetchallvariable name()}}}}}}}), attachment_filename="g.png", as_attachment=True)



# result = cur.execute("SELECT * FROM `osama_blog`.`articles` \
#                       WHERE(CONVERT(`author` USING utf8)\
#                       LIKE '% %s %' )", [request.form['search']])
# from phpmyadmin
# SELECT * FROM `osama_blog`.`articles` WHERE(CONVERT(`author` USING utf8) LIKE '% + OSAMA.MOHAMED + %')
# SELECT * FROM `osama_blog`.`articles` WHERE (CONVERT(`id` USING utf8) LIKE 'OSAMA.MOHAMED' OR CONVERT(`title` USING utf8) LIKE 'OSAMA.MOHAMED' OR CONVERT(`author` USING utf8) LIKE 'OSAMA.MOHAMED' OR CONVERT(`body` USING utf8) LIKE 'OSAMA.MOHAMED' OR CONVERT(`files` USING utf8) LIKE 'OSAMA.MOHAMED' OR CONVERT(`written_date` USING utf8) LIKE 'OSAMA.MOHAMED')
