from flask import request, jsonify, Blueprint

from controllers.auth_controller import token_required
from models.user_model import Users
from repositories.user_repositories import UserRepository
from utils.validation_helpers import is_valid_email

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = Users.query.filter_by(name=data['name']).first()
    if existing_user:
        return jsonify({'error': 'User with that name already exists'}), 409

    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email address'}), 400

    UserRepository.create(data['name'], data['email'], data['password'], data['description'])

    return jsonify({'message': 'New user created'}), 201


@user_blueprint.route('/users', methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' not in data and 'description' not in data:
        return jsonify({'error': 'Bad request'}), 400

    user = Users.query.filter_by(id=current_user.id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404
    existing_user = Users.query.filter(Users.name == data['name'], Users.id != user.id).first()
    if existing_user:
        return jsonify({'error': 'User with that name already exists'}), 409

    UserRepository.update(user, data)

    return jsonify({'message': 'Successfully updated'}), 200


@user_blueprint.route('/users/<name>', methods=['GET'])
@token_required
def get_one_user(current_user, name):

    user_data = UserRepository.get_one(name)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200


@user_blueprint.route('/users', methods=['GET'])
@token_required
def get_many_users(current_user):
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Bad request!'}), 400

    users_data = UserRepository.get_many_by_name(name)

    return jsonify(users_data), 200


@user_blueprint.route('/users/<user_id>/follow', methods=['POST'])
@token_required
def follow_user(current_user, user_id):
    follower_id = current_user.id

    if not user_id:
        return jsonify({'error': 'Bad request'}), 400

    if user_id == current_user.id:
        return jsonify({'error': 'Bad request'}), 400

    UserRepository.follow(follower_id, user_id)

    return jsonify({}), 204


@user_blueprint.route('/users/<user_id>/unfollow', methods=['DELETE'])
@token_required
def unfollow_user(current_user, user_id):
    follower_id = current_user.id

    if not user_id:
        return jsonify({'error': 'Bad request'}), 400

    if follower_id == user_id:
        return jsonify({'error': 'Bad request'}), 400

    UserRepository.unfollow(follower_id, user_id)

    return jsonify({}), 204









