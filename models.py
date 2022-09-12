from app import app, db

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
