from flask import Blueprint, request, jsonify
from controllers.auth_controller import token_required
from models.post_model import Posts
from repositories.post_repositories import PostRepository


post_blueprint = Blueprint('post', __name__)


@post_blueprint.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    PostRepository.create(data['text'], current_user.id)

    return jsonify({'message': 'Post created!'}), 201


@post_blueprint.route('/posts/<post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    post = PostRepository.get_post_by_id(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    PostRepository.update(post, data)

    return jsonify({'message': 'Post updated successfully'}), 200


@post_blueprint.route('/posts/<post_id>', methods=['GET'])
@token_required
def get_post_by_id(current_user, post_id):
    post_data = PostRepository.get_post_by_id(post_id, user_id=str(current_user.id))

    if not post_data:
        return jsonify({'error': 'No post found!'}), 404

    return jsonify(post_data), 200


@post_blueprint.route('/posts/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    post = Posts.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    PostRepository.delete(post)

    return jsonify({'message': "Post has been deleted"}), 200


@post_blueprint.route('/posts/<post_id>/likes', methods=['POST'])
@token_required
def like_post(current_user, post_id):

    action = request.args.get('action')
    if not action:
        return jsonify({'error': 'Bad request1'}), 400

    post = PostRepository.get_post_by_id_without_comments(post_id)

    if not post:
        return jsonify({'error': 'Not found'}), 400

    user_liked = False
    if str(current_user.id) in post['likes']:
        user_liked = True

    if action.lower() == 'like':
        if user_liked is True:
            return jsonify({'error': 'Bad request'}), 400
        PostRepository.like(post, current_user.id)
        return jsonify({}), 204
    elif action.lower() == 'unlike':
        if user_liked is False:
            return jsonify({'error': 'Bad request'}), 400
        PostRepository.unlike(post, current_user.id)
        return jsonify({}), 204

    return jsonify({'error': 'Bad request'}), 400
