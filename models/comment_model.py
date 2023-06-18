import uuid
from datetime import datetime
from sqlalchemy import DateTime
from extensions import db
from sqlalchemy.dialects.postgresql import UUID, JSON


class Comments(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.String(200))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('posts.id'))
    likes = db.Column(JSON)