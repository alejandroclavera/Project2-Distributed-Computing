from werkzeug.wrappers import response
import pytest
from app.models.content import Content, Keyword
from app.authentication.auth import Auth
from app.models.user import User
from test import setup_app
from . import content_url_api

#######################################
#   TEST delete content information   #
#######################################
test_contents = [
    {'title': 'title1', 'description': 'description1', 'keywords':[
        {'keyword':'key', 'value':'val'}, 
        {'keyword':'key2', 'value': 'val2'}
    ]},
    {'title': 'title2', 'description': 'description2'},
    {'title': 'title3', 'description': 'description3'},
    {'title': 'title4', 'description': 'description4'}
]

@pytest.fixture
def setup_test(setup_app):
    # Create app
    client = setup_app
    content_list = []
    user = User('test_user', 'passwd')
    user.save()
    headers = {'user-token': Auth.generate_token(user.id)}
    for content_to_add in test_contents:
        content_to_add['owner'] = user
        content_to_add['node'] = None
        content = Content(**content_to_add)
        content.save()
        content_list.append(content)
    return client, headers, content_list
    

def test_delete_single_content(setup_test):
    client, headers, content_list = setup_test
    content_id = str(content_list[0].id)
    response = client.delete(content_url_api + content_id, headers=headers)
    
    # Check status code
    assert response.status_code == 200
    
    # Check if the number of contents is decreased
    id_contents = [content.id for content in content_list[1:]]
    current_contents = Content.query.filter(Content.id.in_(id_contents)).all()
    assert len(current_contents) == len(content_list) - 1
    
    # Check if the content it is removed
    assert Content.query.get(content_id) is None
    
    # Check if its keywords are removed
    assert not Keyword.query.filter_by(owner=content_id).all()


def test__delete_multiple_contents(setup_test):
    client, headers, content_list = setup_test
    for content in content_list[:3]:
        response = client.delete(content_url_api + str(content.id), headers=headers)
        assert response.status_code == 200
    
    # Check is the contents are deleted
    deleted_contents_id = [content.id for content in content_list[:3]]
    current_contents_id = [content.id for content in content_list[3:]]
    assert not Content.query.filter(Content.id.in_(deleted_contents_id)).all()
    assert Content.query.filter(Content.id.in_(current_contents_id)).all()


def test_delete_not_registered_contents(setup_test):
    client, headers, content_list = setup_test
    response = client.delete(content_url_api + str(content_list[-1].id + 1), headers=headers)
    assert response.status_code == 404


def test_delete_not_owner_content(setup_test):
    client, _, content_list = setup_test
    user = User('test', 'passw')
    user.save()
    headers = {'user-token': Auth.generate_token(user.id)}
    for content in content_list:
        response = client.put(content_url_api + str(content.id), headers=headers)
        assert response.status_code == 403


def test_delete_empty_db(setup_app):
    client = setup_app
    user = User('test', 'passw')
    user.save()
    headers = {'user-token': Auth.generate_token(user.id)}

    response = client.delete(content_url_api + '1', headers=headers)
    assert response.status_code == 404


def test_bad_user_token(setup_test):
    client, _, _ = setup_test
    headers= {'user-token': 'bad_user_token'}
    
    # Test without user token
    response = client.delete(content_url_api + '1')
    assert response.status_code == 401
    
    # Test bad user token
    bad_usertoken_header = {'user-token': 'badtoken'}
    response = client.delete(content_url_api + '1', headers=bad_usertoken_header)
    assert response.status_code == 400
