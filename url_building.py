from flask import Flask, redirect, url_for 
app = Flask(__name__) 
@app.route('/admin') 
def hello_admin(): 
    return 'Hello Admin'
@app.route('/osama')
def hello_osama():
  return 'Hello OSAMA!'
@app.route('/guest/<guest>') 
def hello_guest(guest): 
    return 'Hello %s as Guest' % guest 
@app.route('/user/<name>') 
def hello_user(name): 
    if name=='admin': 
        return redirect(url_for('hello_admin'))
    elif name=='osama':
        return redirect(url_for('hello_osama'))
    else: 
        return redirect(url_for('hello_guest',guest=name)) 
if __name__ == '__main__': 
    app.run(debug=True)
