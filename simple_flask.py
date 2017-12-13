from flask import Flask 
app = Flask(__name__) 
 
@app.route('/') 
def hello_world(): 
    return "Hello World"
##app.add_url_rule('/', 'hello', hello_world) 
if __name__ == '__main__': 
    app.run(debug = False)
##    app.run(debug = True)



##from flask import Flask
##app = Flask(__name__)
## 
##@app.route("/")
##def hello():
##    return "Hello OSAMA!"
## 
##if __name__ == "__main__":
##    app.run(debug=True)
