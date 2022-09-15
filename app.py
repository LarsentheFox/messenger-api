from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] ="sqlite:///messenger.db" 

db = SQLAlchemy(app)

cors: CORS = CORS()

cors.init_app(app, resources={r"/*": {"origins": "http://localhost:8080"}})


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), index = True, unique = True)
    password = db.Column(db.String(50), index = True, unique = False) 

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


@app.route("/messages", methods=["GET"])
def home():
    message_records = Message.query.all()
    messages = []
    for message in message_records:
        user = User.query.filter_by(id=message.user_id).first()
        messages.append({
            "message_content": message.content,
            "user": message.user_id,
            "username": user.username
        })
    if not messages:
        return '<h1>No messages</h1>'
    return jsonify({
        "messages": messages,
    })

@app.route("/create_message", methods=["POST"])
def create_message():
    try:
        payload = request.json
        message = Message(content=payload["message"], user_id=payload["user"])
        db.session.add(message)
        db.session.commit()
        return jsonify({
            "message": message
        })
    except Exception as e:
        return str(e)


@app.route("/login/<username>/<password>", methods=["POST"])
def login(username, password):
    try:
        user = User.query.filter_by(username = username, password = password).first()
        if user:
            return jsonify({
                "username": user.username,
                "id": user.id
                })
    except Exception as e:
        return str(e)
    


@app.route("/create_user", methods=["POST"])
def create_user():
    try:
        payload = request.json
        user = User(username=payload["username"], password=payload["password"])
        db.session.add(user)
        db.session.commit()
        return user.username
    except Exception as e:
        return str(e)
        
