from flask import Flask, g, render_template, request, abort


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, OSAMA!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    # name = request.args.get['name']
    if name is None:
        return "Hello sranger!"
    elif name == name:
        return 'Hello, %s!' % name
    else:
        abort(404)



if __name__ == '__main__':
    app.run(debug=True)