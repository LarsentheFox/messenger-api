from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] ="sqlite:///messenger.db" 

db = SQLAlchemy(app)

cors: CORS = CORS()

cors.init_app(app, resources={r"/*": {"origins": "http://localhost:8080"}})

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), index = True, unique = True)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __repr__(self):
        return "{}".format(self.username)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(255), index = True, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "{}".format(self.content)


db.create_all()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/", methods=["GET"])
def home():
    messages = Message.query.all()
    if not messages:
        return '<h1>No messages</h1>'
    return f'<h1>{Message.query.all()}</h1>'

@app.route("/message", methods=["GET"])
def message():
    message = Message.query.first()
    return str(message.id)