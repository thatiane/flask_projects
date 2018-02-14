

from flask import render_template, redirect, request, url_for, flash, session
from passlib.hash import sha256_crypt
from python.database.flask_database import *

login_admin = Blueprint('login_admin', __name__)


# admin login page

@login_admin.route('/admin/login', methods=['GET', 'POST'])
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
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
                cur.close()
                error = 'Wrong Password!'
                return render_template('admin_login.html', error=error)
        else:
            cur.close()
            error = 'Username Can Not Be Found!'
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')