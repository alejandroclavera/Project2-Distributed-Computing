from flask import Blueprint, request
from flask.json import jsonify
from app.services import node_services

node_controller = Blueprint('node_controller', __name__)

@node_controller.route('/register/', methods=['POST'])
def register_node():
    """
    Register a new node in a WS
    """
    node_info, status_code = node_services.register_node()
    if status_code == 400:
        return jsonify({'error': 'BAD REQUEST'}), 400
    else:
        return jsonify(node_info)

