import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120)(unique=True))
    password = db.Column(db.String(180))
    description = db.Column(db.String(120))
    created_at = db.Column(db.String(120))
    updated_at = db.Column(db.String(120))
