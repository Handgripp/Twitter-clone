import uuid

from werkzeug.security import generate_password_hash

from models.user_model import Users, db


class UserRepository:

    @staticmethod
    def create_user(name, email, password, description):
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = Users(id=str(uuid.uuid4()), name=name, email=email, password=hashed_password, description=description)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def update_user(user, data):
        user.name = data['name']
        user.description = data['description']
        db.session.commit()

    @staticmethod
    def get_one_user(name):
        user = Users.query.filter_by(name=str(name)).first()
        if not user:
            return None

        user_data = {
            'name': user.name,
            'description': user.description
        }

        return user_data
