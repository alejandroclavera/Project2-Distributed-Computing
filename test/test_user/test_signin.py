import pytest
from test import setup_app
from test.test_user import user_url_api
from app.models.user import User
from app.authentication.auth import Auth

test_users = [
    {'user_name':'user1', 'password':'pssw1'},
    {'user_name':'user2', 'password':'pssw2'},
]


@pytest.fixture
def setup_test(setup_app):
    # Create app
    client = setup_app
    user_list = []
    for user_to_add in test_users:
        user = User(*user_to_add.values())
        user.save()
        user_list.append(user)
    return client, user_list

def test_sigin_users(setup_test):
    client, user_list = setup_test
    for index, user in enumerate(user_list):
        response = client.post(user_url_api + 'signin/', json=test_users[index])
        assert response.status_code == 200
        response_json = response.get_json()
        assert 'user-token' in response_json
        user_token = response_json['user-token']
        token_data = Auth.decode_token(user_token)
        assert 'data' in token_data
        user_id = token_data['data']['user_id']
        assert user_id == user.id

def test_bad_password(setup_test):
    client, _ = setup_test
    bad_user = {'user_name':test_users[0]['user_name'], 'password': 'badpssw'}
    response = client.post(user_url_api + 'signin/', json=bad_user)
    assert response.status_code == 400

def test_not_registered_user(setup_test):
    client, _ = setup_test
    not_registered_user = {'user_name': 'not_registered', 'password': 'pssw'}
    response = client.post(user_url_api + 'signin/', json=not_registered_user)
    assert response.status_code == 400

def test_bad_request(setup_test):
    client, _ = setup_test
    # Check post without json body
    response = client.post(user_url_api + 'signin/')
    assert response.status_code == 400

    # Check bad format
    response = client.post(user_url_api + 'signin/', json={})
    assert response.status_code == 400
    response = client.post(user_url_api + 'signin/', json={'user_name': 'test'})
    assert response.status_code == 400
    response = client.post(user_url_api + 'signin/', json={'password': 'test'})
    assert response.status_code == 400