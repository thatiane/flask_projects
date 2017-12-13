from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'python2flask@gmail.com'
app.config['MAIL_PASSWORD'] = 'flask2python'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)
@app.route("/")
def index():
    msg = Message('Hello',sender='sender@gmail.com',recipients=['python2flask@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "the message has been Sent to %s" % "python2flask@gmail.com"
if __name__ == '__main__':
    app.run()
