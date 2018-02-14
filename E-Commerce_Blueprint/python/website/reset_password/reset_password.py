# some imports
from flask import render_template, request, flash, redirect, url_for
from passlib.hash import sha256_crypt
from wtforms import Form, validators, PasswordField
from python.database.flask_database import *


reset_user_password = Blueprint('reset_user_password', __name__)


# reset password form validators

class reset_password(Form):
    password = PasswordField('Password',
                             [validators.DataRequired(), validators.Length(min=6, max=100),
                              validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

# write new password page

@reset_user_password.route("/user_reset_password/<id>", methods=['GET', 'POST'])
def user_reset_password(id):
    form = reset_password(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        cur.execute("SELECT reset_password_permission FROM users WHERE id = %s AND permission='user'", [id])
        permission = cur.fetchone()
        password_permission = permission['reset_password_permission']
        if password_permission == 'reset':
            encrypted_password = sha256_crypt.encrypt(str(form.password.data))
            cur.execute("UPDATE users SET password = %s WHERE id = %s AND permission='user'", [encrypted_password, id])
            cur.execute("UPDATE users SET reset_password_permission = 'no_reset' WHERE id = %s AND permission='user'", [id])
            mysql.connection.commit()
            cur.close()
            flash("You Have Successfully Changed Your Password Now!", "success")
            return redirect(url_for('web_home.home'))
        else:
            cur.close()
            flash("You Have Changed Your Password before!", "warning")
            return redirect(url_for('web_home.home'))
    return render_template('user_reset_password.html', form=form)
