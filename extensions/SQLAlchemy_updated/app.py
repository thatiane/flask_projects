from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'],
                               request.form['city'],
                               request.form['addr'],
                               request.form['pin'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route('/del')
def delete():
    db.session.query(students).delete()
    db.session.commit()
    flash('All Records Has Been Successfully Deleted')
    return redirect(url_for('show_all'))



@app.route('/del_one')
def delete_one():
    # students.query.filter_by(id=1).delete()
    # students.query.filter_by(name='.....').delete()
    # students.query.filter_by(city='.....').delete()
    # students.query.filter_by(addr='.....').delete()
    # students.query.filter_by(pin='.....').delete()
    db.session.commit()
    flash('The Selected Record Has Been Successfully Deleted')
    return redirect(url_for('show_all'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) 


# #for all records delete
# db.session.query(Table_name).delete()
# db.session.commit()
# 
# #for specific value delete
# db.session.query(Table_name).filter_by(id==123).delete()
# db.session.commit()
