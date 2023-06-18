import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String(200))
    created_at = db.Column(db.String(20))
    updated_at = db.Column(db.String(20))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('post.id'))
    likes = db.Column(db.String(60))