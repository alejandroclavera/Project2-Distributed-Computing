from flask import json
from werkzeug.wrappers import response
from app.authentication.auth import Auth
from test import setup_app
from app.models.user import User
from . import user_url_api


test_user = {
    'user_name':'user1',
    'password': 'pssw1'
}

def test_create_new_user(setup_app):
    app = setup_app
    with app.test_client() as client:
        response = client.post(user_url_api + 'signup/', json=test_user)
        assert response.status_code == 200
        # Check the body response
        response_json = response.get_json()
        assert 'user-token' in response_json
        user_token_data = Auth.decode_token(response_json['user-token'])
        assert 'error' not in user_token_data
        # Check if the user are created in the database
        user_id = user_token_data['data']['user_id']
        user = User.query.get(user_id)
        assert user.user_name == test_user['user_name']
        assert user.check_hash(test_user['password'])


def test_bad_request(setup_app):
    app = setup_app
    with app.test_client() as client:
        # Check post without json body
        response = client.post(user_url_api + 'signup/')
        assert response.status_code == 400
        # Check bad format
        response = client.post(user_url_api + 'signup/', json={})
        assert response.status_code == 400
        response = client.post(user_url_api + 'signup/', json={'user_name': 'test'})
        assert response.status_code == 400
        response = client.post(user_url_api + 'signup/', json={'password': 'test'})
        assert response.status_code == 400


def test_register_existing_user(setup_app):
    app = setup_app
    user = User(test_user['user_name'], test_user['password'])
    user.save()
    print(user.serialize)
    with app.test_client() as client:
        response = client.post(user_url_api + 'signup/', json=test_user)
        assert response.status_code == 400