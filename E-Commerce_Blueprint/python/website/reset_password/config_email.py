
from flask_mail import Mail
from flask import Flask


# application configuration to send email with gmail
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'osama.buy.sell@gmail.com'
app.config['MAIL_PASSWORD'] = 'chnuxoeikqtyeclg'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)