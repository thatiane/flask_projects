from flask import Flask, redirect, url_for, request 
app = Flask(__name__)

@app.route('/success/<name>') 
def success(name):
    return 'welcome %s' % name

@app.route('/success_get/<name>') 
def success_get(name):
    return 'welcome get %s' % name

@app.route('/login',methods=['POST', 'GET']) 
def login(): 
    if request.method=='POST': 
        user=request.form['nm'] 
        return redirect(url_for('success',name=user)) 
    else: 
        user=request.args.get('nm') 
        return redirect(url_for('success_get',name=user))
    
if __name__ == '__main__': 
    app.run(debug=True)
