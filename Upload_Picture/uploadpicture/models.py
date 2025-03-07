from uploadpicture import db
from flask_login import UserMixin
from datetime import timezone
from sqlalchemy.sql import func

class Img(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique = True, nullable = False)
    name = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    mimetype = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100), unique = True, nullable = False)
    Password = db.Column(db.String(100), nullable = False)
    Pictures = db.relationship("Img")

    def __init__(self, name, password):
        self.Name = name
        self.Password = password