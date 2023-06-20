import uuid

from werkzeug.security import generate_password_hash

from models.follow_model import Follows
from models.user_model import Users, db


class UserRepository:

    @staticmethod
    def create(name, email, password, description):
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = Users(id=str(uuid.uuid4()), name=name, email=email, password=hashed_password, description=description)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def update(user, data):
        user.name = data['name']
        user.description = data['description']
        db.session.commit()

    @staticmethod
    def get_one(name):
        user = Users.query.filter_by(name=str(name)).first()
        if not user:
            return None

        user_data = {
            'id': user.id,
            'name': user.name,
            'description': user.description
        }

        return user_data

    @staticmethod
    def get_many_by_name(name):
        users = Users.query.filter(Users.name.ilike(f'%{name}%')).limit(5).all()

        users_data = []

        for user in users:
            parsed_user = {
                'id': user.id,
                'name': user.name,
                'description': user.description
            }
            users_data.append(parsed_user)

        return users_data

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
