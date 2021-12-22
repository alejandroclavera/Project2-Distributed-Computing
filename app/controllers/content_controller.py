from flask import Blueprint, request
from flask.json import jsonify

from app.models import content
from ..services import content_services

content_controller = Blueprint('content_controller', __name__)

@content_controller.route('/', methods=['GET'])
def find_content():
    contents = content_services.find_content(request.args)
    return jsonify([content.serialize for content in contents])

@content_controller.route('/', methods=['POST'])
def add_new_content():
    """
    Registry a new content in the WS
    """
    content = content_services.post_new_content(request.form)
    if content is None:
        return jsonify({'error_message': 'can\'t create new content'}), 400
    return jsonify(content.serialize), 200
