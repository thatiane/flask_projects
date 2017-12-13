from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                print("Opened database successfully")
                con.execute('CREATE TABLE IF NOT EXISTS students(name TEXT, addr TEXT, city TEXT, Phone TEXT);')
                print("Table created successfully")
                cur.execute("INSERT INTO students(name,addr,city,Phone) VALUES(%r, %r, %r, %r);"%(nm, addr, city, pin))
                # cur.execute("INSERT INTO students(name,addr,city,pin) VALUES({}, {}, {}, {});".format(nm, addr, city, pin))
                con.commit()
                msg = "Record successfully added".title()
        except:
            con.rollback()
            msg = "error in insert operation".title()
        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    con.execute('CREATE TABLE IF NOT EXISTS students(name TEXT, addr TEXT, city TEXT, Phone TEXT);')
    cur.execute("select * from students")
    con.commit()
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)
@app.route('/del')
def delete():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from students")
    con.commit()
    msg = "now all data in database table has been deleted".title()
    return render_template("result.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
