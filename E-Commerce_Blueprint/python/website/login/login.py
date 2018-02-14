from flask import render_template, request, redirect, session, url_for, flash
from passlib.hash import sha256_crypt
from python.database.flask_database import *

login = Blueprint('login', __name__)

# user login page

@login.route('/user_login', methods=['GET', 'POST'])
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
                return redirect(url_for('account.user_account'))
            else:
                error = 'Wrong Password!'
                return render_template('user_login.html', error=error)
        else:
            error = 'Username Can Not Be Found!'
            return render_template('user_login.html', error=error)
    return render_template('user_login.html')