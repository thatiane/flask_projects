from flask import Flask, render_template, request, flash
from flask_wtf import Form 
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField 
from wtforms import validators, ValidationError 

app = Flask(__name__)
app.secret_key = 'development key'

class ContactForm(Form): 
    name = StringField("Name Of Student", [validators.required("Please enter your name.")]) 
    Gender = RadioField('Gender', choices=[('M','Male'),('F','Female')]) 
    Address = TextAreaField("Address") 
    email = StringField("Email",[validators.required("Please enter your email address."), validators.Email("Please enter your email address.")]) 
    Age = IntegerField("age") 
    language = SelectField('Languages', choices=[('cpp', 'C++'), ('py', 'Python')]) 
    submit = SubmitField("Send")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
            
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     form = ContactForm()
#     if request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             return render_template('contact.html', form=form)
             #return "wrong entires!!!"
#         else:
#             return 'Form posted.'
#     elif request.method == 'GET':
#         return render_template('contact.html', form=form)
# if __name__ == '__main__':
#     app.run(debug=True)