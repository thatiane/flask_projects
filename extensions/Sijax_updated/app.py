import os, sys
from flask import Flask, g, render_template
import flask_sijax
path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)
app = Flask(__name__)
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)
@app.route("/")
def hello():
    return "Hello Osama!<br><br><a href='/sijax'>Go to Sijax test</a>"
@flask_sijax.route(app, "/sijax")
def hello_sijax():
    def hello_handler(obj_response, hello_from, hello_to):
        obj_response.alert('Hello from %s to %s' % (hello_from, hello_to))
        obj_response.css('a', 'color', 'green')
    def goodbye_handler(obj_response):
        obj_response.alert('Goodbye, OSAMA MOHAMED!')
        obj_response.css('a', 'color', 'red')
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('say_hello', hello_handler)
        g.sijax.register_callback('say_goodbye', goodbye_handler)
        return g.sijax.process_request()
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)
