from flask import Blueprint, jsonify
from controllers.auth_controller import token_required
from models.follow_model import Follows
from repositories.follow_repositories import FollowRepository

follow_blueprint = Blueprint('follow', __name__)


@follow_blueprint.route('/users/<user_id>/follow', methods=['POST'])
@token_required
def follow_user(current_user, user_id):
    existing_follow = Follows.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    follower_id = current_user.id

    if existing_follow is not None:
        return jsonify({'error': 'Bad request'}), 400

    if not user_id:
        return jsonify({'error': 'Bad request'}), 400

    if user_id == current_user.id:
        return jsonify({'error': 'Bad request'}), 400

    FollowRepository.follow(follower_id, user_id)

    return jsonify({}), 204


@follow_blueprint.route('/users/<user_id>/unfollow', methods=['DELETE'])
@token_required
def unfollow_user(current_user, user_id):
    existing_follow = Follows.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    follower_id = current_user.id

    if existing_follow is None:
        return jsonify({'error': 'Bad request'}), 400

    if not user_id:
        return jsonify({'error': 'Bad request'}), 400

    if follower_id == user_id:
        return jsonify({'error': 'Bad request'}), 400

    FollowRepository.unfollow(follower_id, user_id)

    return jsonify({}), 204
