from flask_sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy import String

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    user = db.relationship('User', backref='tasks')
