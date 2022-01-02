from flask import Blueprint, request
from flask.json import jsonify
from app.authentication.auth import Auth
from app.services import user_services
from app.controllers import require_request_json_body

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/signup/', methods=['POST'])
@require_request_json_body
def singup():
    '''
    Register new user
    '''
    user = user_services.create_new_user(request.json)
    if user is None:
        return jsonify({'error': 'Bad request'}),400
    # Generate token    
    token = Auth.generate_token(user.id)
    return jsonify({'user-token': token}), 200


@user_controller.route('/signin/', methods=['POST'])
@require_request_json_body
def signin():
    """
    Login a user
    """
    user = user_services.autenticate_user(request.json)
    if user is None:
        return jsonify({'error': 'Bad request'}),400
    # Generate token    
    token = Auth.generate_token(user.id)
    return jsonify({'user-token': token}), 200


@user_controller.route('/<id>/', methods=['GET'])
def get_user_content_list(id):
    contents = user_services.get_user_contents(id)
    if contents is None:
        return jsonify({'error_message': 'Bad request'}), 400
    return jsonify([content.serialize for content in contents]), 200
