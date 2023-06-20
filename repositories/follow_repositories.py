from extensions import db
from models.follow_model import Follows


class FollowRepository:

    @staticmethod
    def follow(follower_id, followed_id):
        follow = Follows(follower_id=follower_id, followed_id=followed_id)
        db.session.add(follow)
        db.session.commit()
        return follow

    @staticmethod
    def unfollow(follower_id, followed_id):
        follow = Follows.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()

        if follow:
            db.session.delete(follow)
            db.session.commit()
            return True
        else:
            return False
