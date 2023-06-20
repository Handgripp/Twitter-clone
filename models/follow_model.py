from sqlalchemy import UUID

from extensions import db


class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    followed_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
