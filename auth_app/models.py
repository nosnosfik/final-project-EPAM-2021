from app import db
from flask_login import UserMixin

ROLES = {0: 'user', 1: 'admin'}


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.SmallInteger, default=ROLES[0])
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
