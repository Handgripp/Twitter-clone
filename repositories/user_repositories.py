import uuid
from werkzeug.security import generate_password_hash
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
    def get_one_by_name(name):
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
    def get_one_by_id(user_id):
        user = Users.query.get(user_id)
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


