# some imports
from flask import render_template, request, flash, redirect, url_for
from flask_mail import Message
from python.database.flask_database import *
from python.website.reset_password.config_email import *



email_password = Blueprint('email_password', __name__)


# send e-mail with link to reset user account password

@email_password.route("/user_forget_password_email", methods=['GET', 'POST'])
def user_forget_password_email():
    if request.form['username_reset'] == '':
        flash('You did not write a username !', 'warning')
        return render_template('user_forget_password.html')
    user_name = request.form['username_reset']
    cur = mysql.connection.cursor()
    r = cur.execute("SELECT id, email, username FROM users WHERE username = %s AND permission='user' ", [user_name])
    res = cur.fetchone()
    if r > 0:
        email = res['email']
        msg = Message()
        msg.sender = 'osama.buy.sell@gmail.com'
        msg.subject = "Reset Your Password"
        msg.recipients = [email]
        msg.body = "Reset Your Password : http://localhost:5000/user_reset_password/%s \n message sent from Flask-Mail Automatic sender!" % (res['id'])
        mail.send(msg)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET reset_password_permission = 'reset' WHERE username = %s AND permission='user'", [user_name])
        mysql.connection.commit()
        cur.close()
        flash("The Reset Message has been Sent to your email!", "success")
        flash("Please check your email!", "warning")
        return redirect(url_for('web_home.home'))
    else:
        cur.close()
        flash("This username Not Found!", "warning")
        return redirect(url_for('web_home.home'))