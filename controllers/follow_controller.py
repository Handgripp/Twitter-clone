from flask import Blueprint, jsonify

follow_blueprint = Blueprint('follow', __name__)


@follow_blueprint.route('/posts', methods=['POST'])
def create_post():
    return jsonify({'message': 'New user created'}), 201