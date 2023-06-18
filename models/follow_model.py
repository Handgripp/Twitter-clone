from extensions import db


class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.ForeignKey('user.id'))
    followed_id = db.Column(db.ForeignKey('user.id'))
