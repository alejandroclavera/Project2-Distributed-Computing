from flask import Blueprint, request
from flask.json import jsonify

from app.models import content
from ..services import content_services

content_controller = Blueprint('content_controller', __name__)


@content_controller.route('/', methods=['GET'])
def find_content():
    contents = content_services.find_content(request.args)
    if contents is None:
        return jsonify({'error_message': 'Bad request'}), 400
    return jsonify([content.serialize for content in contents])


@content_controller.route('/', methods=['POST'])
def add_new_content():
    """
    Registry a new content in the WS
    """
    content = content_services.post_new_content(request.json)
    if content is None:
        return jsonify({'error_message': 'can\'t create new content'}), 400
    return jsonify(content.serialize), 200


@content_controller.route('/<id>', methods=['GET'])
def get_content_info(id):
    """
    Obtain the content with the id
    """
    content = content_services.get_content_by_id(id)
    if content is None:
        return jsonify({'error_message': f'not found the content with the id {id}'}), 404
    return jsonify(content.serialize), 200


@content_controller.route('/<id>', methods=['PUT'])
def modify_content(id):
    """
    Modify the content with the id
    """
    content = content_services.modify_content(id, request.json)
    if content is None:
        return jsonify({'error_message': f'not found the content with the id {id}'}), 404
    return jsonify(content.serialize), 200


@content_controller.route('/<id>', methods=['DELETE'])
def delete_content(id):
    """
    Delete the content of the id
    """
    content_is_deleted = content_services.delete_content_by_id(id)
    if not content_is_deleted:
        return jsonify({'error_message': f'not found the content for delete with the id {id}'}), 404
    return jsonify({'message': 'Content deleted'}), 200
