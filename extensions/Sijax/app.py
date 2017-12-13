import os, sys
from flask import Flask, g, render_template
import flask_sijax
path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)
app = Flask(__name__)
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

@app.route('/')
def index():
    return "Hello Osama!<br><br><a href='/hello'>Go to Hello page</a>"

@flask_sijax.route(app, '/hello')
def hello():
    def say_hi(obj_response, sayhi):
        obj_response.alert('Hi %s!'%(sayhi))

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()
    return render_template('sijaxexample.html')


if __name__ == '__main__':
    app.run(debug=True)
