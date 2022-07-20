from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] ="" 


db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"