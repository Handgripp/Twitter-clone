from flask import Blueprint, jsonify, request

from controllers.auth_controller import token_required
from models.comment_model import Comments
from models.post_model import Posts
from repositories.comment_repositories import CommentRepository
from repositories.post_repositories import PostRepository

comment_blueprint = Blueprint('comment', __name__)


@comment_blueprint.route('/comments/<post_id>', methods=['POST'])
@token_required
def create_comment(current_user, post_id):
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    post = PostRepository.get_post_by_id(post_id, user_id=current_user.id)
    if not post:
        return jsonify({'error': 'Post not found!'}), 404

    CommentRepository.create(data['text'], post_id)

    return jsonify({'message': 'Comment created!'}), 201


@comment_blueprint.route('/comments/<comment_id>', methods=['GET'])
@token_required
def get_comment_by_id(current_user, comment_id):
    comment_data = CommentRepository.get_one_by_id(comment_id, current_user.id)

    if not comment_data:
        return jsonify({'error': 'No post found!'}), 404

    return jsonify(comment_data), 200


@comment_blueprint.route('/comments/<comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    comment = CommentRepository.update(comment_id, data)

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    return jsonify({'message': 'Comment updated successfully'}), 200


@comment_blueprint.route('/comments/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    CommentRepository.delete(comment)

    return jsonify({'message': "Comment has been deleted"}), 200


@comment_blueprint.route('/comments/<comment_id>/likes', methods=['POST'])
@token_required
def like_comment(current_user, comment_id):
    action = request.args.get('action')
    if not action:
        return jsonify({'error': 'Bad request'}), 400

    comment = CommentRepository.get_one_by_id(comment_id, current_user.id)
    if not comment:
        return jsonify({'error': 'Not found'}), 400

    user_liked = False
    if str(current_user.id) in comment['likes']:
        user_liked = True
    print(comment)
    if action.lower() == 'like':
        if user_liked is True:
            return jsonify({'error': 'Bad request'}), 400
        CommentRepository.like(comment, current_user.id)
        return jsonify({}), 204
    elif action.lower() == 'unlike':
        if user_liked is False:
            return jsonify({'error': 'Bad request'}), 400
        CommentRepository.unlike(comment, current_user.id)
        return jsonify({}), 204

    return jsonify({'error': 'Bad request'}), 400
