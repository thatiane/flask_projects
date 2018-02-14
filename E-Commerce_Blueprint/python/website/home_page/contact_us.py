# some imports
from flask import render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, TextAreaField, validators
from python.database.flask_database import *

contact_us_home_page = Blueprint('contact_us_home_page', __name__)



# contact us form validators

class Contact_us(Form):
    name = StringField('Name', [validators.DataRequired()])
    mobile_phone = StringField('Phone', [validators.DataRequired()])
    email = StringField('E-mail', [validators.DataRequired()])
    message = TextAreaField('Message', [validators.DataRequired()])


# contact us form from home page

@contact_us_home_page.route('/contact_us', methods=['post', 'get'])
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
        return redirect(url_for('web_home.home'))
    return render_template('contact_us.html', form=form)
