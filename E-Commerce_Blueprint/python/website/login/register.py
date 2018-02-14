# some imports
from flask import render_template, request, flash, redirect, url_for
from passlib.hash import sha256_crypt
from wtforms import Form, validators, StringField, PasswordField
from werkzeug.utils import secure_filename
from shutil import rmtree, copy
import os
from python.database.flask_database import *


register = Blueprint('register', __name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@register.route('/user_register', methods=['post', 'get'])
def user_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data

        folder = os.path.exists(app.root_path + r"\static\uploads\users\{}".format(username))
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
                    rmtree(app.root_path + r"\static\uploads\users\{}".format(username))
                    os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
                except:
                    os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
                filename = secure_filename(file.filename)
                dir = app.root_path + r"\static\uploads\users\{}".format(username)
                file.save(os.path.join(dir, filename))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                             email, gender, country, username, password, files)\
                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            ("user", first_name, last_name, email, gender,\
                             country, username, password, filename))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created Account successfully!', 'success')
                return redirect(url_for('user_login'))
            elif file.filename == '' or 'file' not in request.files:
                try:
                    rmtree(app.root_path + r"\static\uploads\users\{}".format(username))
                    os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
                except:
                    os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
                copy(app.root_path + r'\static\admin.png', app.root_path + r'\static\uploads\users\{}\admin.png'.format(username))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                                             email, gender, country, username, password, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            ("user", first_name, last_name, email, gender, \
                             country, username, password, 'admin.png'))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created Account successfully!', 'success')
                return redirect(url_for('login.user_login'))
    return render_template('user_register.html', form=form)