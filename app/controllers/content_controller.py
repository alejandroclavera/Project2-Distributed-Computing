from flask import Blueprint, request, send_file
from flask.json import jsonify
from app.authentication.auth import Auth
from ..services import content_services

content_controller = Blueprint('content_controller', __name__)


@content_controller.route('/', methods=['GET'])
def find_content():
    contents = content_services.find_content(request.args)
    if contents is None:
        return jsonify({'error_message': 'Bad request'}), 400
    return jsonify([content.serialize for content in contents]), 200


@content_controller.route('/', methods=['POST'])
@Auth.auth_required
def add_new_content():
    """
    Registry a new content in the WS
    """
    content = content_services.post_new_content(request.json)
    if content is None:
        return jsonify({'error_message': 'can\'t create new content'}), 400
    return jsonify(content.serialize), 201


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
@Auth.auth_required
def modify_content(id):
    """
    Modify the content with the id
    """
    content, status_code = content_services.modify_content(id, request.json)
    if status_code == 404:
        return jsonify({'error_message': f'not found the content with the id {id}'}), 404
    elif status_code == 403:
        return jsonify({'error_message': f'can\'t modify the content of other user'}), 403
    return jsonify(content.serialize), 200


@content_controller.route('/<id>', methods=['DELETE'])
@Auth.auth_required
def delete_content(id):
    """
    Delete the content of the id
    """
    status_code = content_services.delete_content_by_id(id)
    if status_code == 404:
        return jsonify({'error_message': f'not found the content with id {id}'}), 404
    elif status_code == 403:
        return jsonify({'error_message': f'can\'t modify the content of other user'}), 403
    return jsonify({'message': 'Content deleted'}), 200


@content_controller.route('/<id>/user/', methods=['GET'])    
def get_user_owner(id):
    owner, status_code = content_services.get_owner(id)
    if status_code == 404:
        return jsonify({'error_message': f'not found the content with id {id}'}), 404
    return jsonify({'owner': owner}), 200


@content_controller.route('/<id>/download', methods=['GET'])
def download_content_info(id):
    """
    Download the information of the id
    """
    content_to_download = content_services.get_content_file_by_id(id)
    if not content_to_download:
        return jsonify({'error_message': f'not found the content for download with id {id}'}), 404
    try:
        return send_file(content_to_download, download_name=f'{id}.json', as_attachment=True), 200
    except Exception as e:
        jsonify({'message': 'Content download'}), 500


@content_controller.route('/download', methods=['GET'])
def download_all_content_info():
    """
    Download all content information
    """
    content_to_download = content_services.get_all_content_file()
    if not content_to_download:
        return jsonify({'error_message': f'not found the content for download'}), 404
    try:
        return send_file(content_to_download, download_name='contents.json', as_attachment=True), 200
    except Exception as e:
        jsonify({'error_message': 'Error to download the contend'}), 500
