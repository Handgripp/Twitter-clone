import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.ForeignKey('follower.id'))
    followed_id = db.Column(db.ForeignKey('followed.id'))
