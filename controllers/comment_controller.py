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

    post = PostRepository.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found!'}), 404

    CommentRepository.create_comment(data['text'], post_id)

    return jsonify({'message': 'Comment created!'}), 201


@comment_blueprint.route('/comments/<comment_id>', methods=['GET'])
@token_required
def get_post_by_id(current_user, comment_id):
    comment = CommentRepository.get_comment_by_id(comment_id)

    if not comment:
        return jsonify({'error': 'No comment found!'}), 404

    post = Posts.query.filter_by(id=comment.post_id).first()
    if not post:
        return jsonify({'error': 'Post not found!'}), 404

    post_data = {
        'id': comment.id,
        'post_id': post.id,
        'text': comment.text,
        'likes': comment.likes,
        'created_at': comment.created_at,
        'updated_at': comment.updated_at,

    }

    return jsonify(post_data), 200


@comment_blueprint.route('/comments/<comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    comment = CommentRepository.update_comment(comment_id, data)

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    return jsonify({'message': 'Comment updated successfully'}), 200


@comment_blueprint.route('/comments/<comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    CommentRepository.delete_comment(comment)

    return jsonify({'message': "Comment has been deleted"}), 200
