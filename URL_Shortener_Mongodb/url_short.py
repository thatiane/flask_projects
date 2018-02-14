from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from pymongo import MongoClient
import datetime
import os
import random
import string


app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017')
db = client.short


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'g.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    r = request.form['url']
    if r is None or r == "" or r == " ":
        return redirect(url_for('index'))
    for short_link in db.short_link.find({"original_link": r}):
        sl2 = short_link
        return render_template('already_exists.html', sl2=sl2)
    else:
        def random_string():
            return ("".join([random.choice(string.ascii_letters + string.digits) for i in range(6)]))
        db.short_link.insert_one({"original_link": r, "short_link": random_string(), "process_date": datetime.datetime.now()})
        db.short_link.find({"original_link": r})
        for short_link in db.short_link.find({"original_link": r}):
            return render_template('result.html', short_link=short_link)



# @app.route('/link/<url_name>', methods=['GET', 'post'])
@app.route('/<url_name>')
def href(url_name):
    for short_link in db.short_link.find({"short_link": url_name}):
        link = short_link['original_link']
        return redirect(link)
    else:
        msg = 'No Urls Found!'
        return render_template('url.html', msg=msg)


if __name__ == '__main__':
    app.secret_key = 'shorten_url'
    app.run(debug=True)
