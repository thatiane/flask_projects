from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pusher


pusher_client = pusher.Pusher(
  app_id='501455',
  key='db14db7ce18aaacd07f7',
  secret='5ade886a76ed83794a3a',
  cluster='us2',
  ssl=True
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://OSAMA:OSAMA@localhost/messages'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    message = db.Column(db.TEXT())
    posted = db.Column(db.DateTime, default=datetime.now())


@app.route('/')
def hello_world():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():
    try:
        username = request.form.get('username')
        message = request.form.get('message')
        pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})
        save_message = Message(name=username, message=message)
        db.session.add(save_message)
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failure'})


if __name__ == '__main__':
    app.run(debug=True)
