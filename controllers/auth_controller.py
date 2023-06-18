import datetime
from functools import wraps
import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.user_model import Users

auth_blueprint = Blueprint('login', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
            current_user = Users.query.filter_by(id=data['id']).first()
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Token is invalid!'}), 401

    return decorated


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data['name'] or not data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401

    user = Users.query.filter_by(name=data['name']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode(
        {'id': str(user.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        'thisissecret',
        algorithm='HS256')

    return jsonify({'token': token}), 200
