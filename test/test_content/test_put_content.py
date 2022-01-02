from werkzeug.wrappers import response
from app.models import user
import pytest
from app.models.user import User
from app.models.content import Content
from app.authentication.auth import Auth
from test import setup_app
from . import content_url_api

#######################################
#   TEST modify content information   #
#######################################
test_contents = [
    {'title': 'title1', 'description': 'description1'},
    {'title': 'title2', 'description': 'description2'},
    {'title': 'title3', 'description': 'description3'},
    {'title' : 'title4', 'description':'description4', 'keywords': [
        {'keyword':'testkey1', 'value':'test_value1'},
        {'keyword':'testkey2', 'value':'test_value2'},
    ]}
]

test_update_info = [
    {'title': 'title1 modified'},
    {'description': 'description2 modified'},
    {'title': 'tilte modified', 'description': 'description modified'},
    {'title' : 'title4', 'description':'description4', 'keywords': [
        {'keyword':'testkey1', 'value':'test_value2'},
        {'keyword':'testkey2', 'value': None},
        {'keyword': 'testkey3', 'value': 'value3'}
    ]}
]

test_update_info_expected =  [
    {'title': 'title1 modified', 'description': 'description1'},
    {'title': 'title2', 'description': 'description2 modified'},
    {'title': 'tilte modified', 'description': 'description modified'},
    {'title' : 'title4', 'description':'description4', 'keywords': [
        {'keyword':'testkey1', 'value':'test_value2'},
        {'keyword': 'testkey3', 'value': 'value3'}
    ]}
]

def equals(content_1, content_2):
    if content_1['title'] != content_2['title']:
        return False
    elif content_1['description'] != content_2['description']:
        return False
    if 'keywords' in content_1 and 'keywords' in content_2:
        return content_1['keywords'] == content_2['keywords']
    return True


@pytest.fixture
def setup_test(setup_app):
    # Create app
    app = setup_app
    user = User('test_user', 'pssw')
    user.save()
    content_list = []
    for content_to_add in test_contents:
        content_to_add['owner'] = user
        content = Content(**content_to_add)
        content.save()
        user.add_content(content)
        content_list.append(content)
    headers = {'user-token': Auth.generate_token(user.id)}
    return app, headers, content_list

@pytest.fixture
def setup_emptydb_test(setup_app):
    app = setup_app
    user = User('test_user', 'pssw')
    user.save()
    headers = {'user-token': Auth.generate_token(user.id)}
    return app, headers

def test_put_contents(setup_test):
    app, headers, content_list = setup_test
    print(headers)
    with app.test_client() as client:
        for index, content in enumerate(content_list):
            content_modification = test_update_info[index]
            response = client.put(content_url_api + str(content.id), json=content_modification, headers=headers)
            assert response.status_code == 200
            modificated_content_json = response.get_json()
            modificated_content = Content.query.get(content.id)
            assert not modificated_content is None
            assert equals(test_update_info_expected[index], modificated_content_json)
            assert equals(test_update_info_expected[index], modificated_content.serialize)


def test_put_not_owner_user(setup_test):
    app, _, content_list = setup_test
    user2 = User('user2', 'passw') 
    user2.save()
    headers = {'user-token': Auth.generate_token(user2.id)}
    with app.test_client() as client:
        for index, content in enumerate(content_list):
            content_modification = test_update_info[index]
            response = client.put(content_url_api + str(content.id), json=content_modification, headers=headers)
            assert response.status_code == 403

        
def test_put_in_empty_dabase(setup_emptydb_test):
    app, headers = setup_emptydb_test
    with app.test_client() as client:
        response = client.put(content_url_api + '1', json=test_update_info[0], headers=headers)
        assert response.status_code == 404


def test_put_not_registered_content(setup_test):
    app, headers, content_list = setup_test
    with app.test_client() as client:
        not_registered_id = str(content_list[-1].id + 1)
        response = client.put(content_url_api + not_registered_id , json=test_update_info[0], headers=headers)
        assert response.status_code == 404


def test_bad_user_token(setup_test):
    app, headers, _ = setup_test
    with app.test_client() as client:
        # Test without user token
        response = client.put(content_url_api + '1' , json=test_update_info[0])
        assert response.status_code == 401
        # Test bad user token
        bad_usertoken_header = {'user-token': 'badtoken'}
        response = client.put(content_url_api + '1' , json=test_update_info[0], headers=bad_usertoken_header)
        assert response.status_code == 400

