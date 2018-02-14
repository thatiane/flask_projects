


from flask import render_template, request
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, validators, PasswordField
from werkzeug.utils import secure_filename
from shutil import rmtree, copy
import os
from python.admin.login.login_check import *
from python.database.flask_database import *


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


add_user_admin = Blueprint('add_user_admin', __name__)



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

@add_user_admin.route('/admin/add_user', methods=['post', 'get'])
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

        folder = os.path.exists(app.root_path + r"\static\uploads\users\{}".format(username))
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
                rmtree(app.root_path + r"\static\uploads\users\{}".format(username))
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
            except:
                os.makedirs(app.root_path + r"\static\uploads\users\{}".format(username))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                dir = app.root_path + r"\static\uploads\users\{}".format(username)
                file.save(os.path.join(dir, filename))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                             email, gender, country, username, password, files)\
                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (permission, first_name, last_name, email, gender,\
                             country, username, password, filename))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created an Account successfully!', 'success')
                return redirect(url_for('dashboard.admin_dashboard'))
            elif file.filename == '' or 'file' not in request.files:
                copy(app.root_path + r'\static\admin.png', app.root_path + r'\static\uploads\users\{}\admin.png'.format(username))
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users(permission, first_name, last_name,\
                                             email, gender, country, username, password, files)\
                                             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                            (permission, first_name, last_name, email, gender, \
                             country, username, password, 'admin.png'))
                mysql.connection.commit()
                cur.close()
                flash('You Have Created an Account successfully!', 'success')
                return redirect(url_for('dashboard.admin_dashboard'))
    return render_template('admin_add_user.html', form=form, admin_name=session['admin_username'], admin_image=session['admin_image'], permission=session['permission'], messages=messages, count_messages=count_messages, count_orders_where_pending=count_orders_where_pending, count_orders_by_user=count_orders_by_user)