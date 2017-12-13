from flask import Flask, flash, redirect, render_template, request, session, abort
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App!"
 
@app.route("/hello/<string:name>/")
def hello(name):
##    return render_template(
##        'test.html',name=name)
     return render_template(
        'test.html',**locals())
 
if __name__ == "__main__":
##    app.run(port=80, debug=True)
    app.run(debug=True)
