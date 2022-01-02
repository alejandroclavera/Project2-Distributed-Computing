from werkzeug.test import Client
import pytest
from test import setup_app
from app.authentication.auth import Auth
from app.models.user import User
from app.models.content import Content
from . import content_url_api

###################################
#   TEST add content information  #
###################################
test_contets = [
    {'title':'title1', 'description': 'description1'},   
    {'title':'title2', 'description': 'description2', 'keywords':[
        {
            'keyword':'key1',
            'value': 'value1'
        },
        {
            'keyword':'key2',
            'value': 'value2'
        }
    ]}
]

bad_contents_post = [
    {'tile':'not description post'},
    {'description': 'post without tile'},
    {'title': 'bad keywords', 'descripion':'', 'keywords':[{'keyword':''}]},
    {}
]

keys_to_check = ['title', 'description', 'keywords']


@pytest.fixture
def setup_test(setup_app):
    test = setup_app
    user = User('test_user', 'passw')
    user.save()
    headers = {'user-token': Auth.generate_token(user.id)}
    return test, headers


def equals(content_1, content_2):
    if content_1['title'] != content_2['title']:
        return False
    elif content_1['description'] != content_2['description']:
        return False
    elif 'keywords' in content_1 and 'keywords' in content_2:
        return content_1['keywords'] == content_2['keywords']
    return True


def check_keys(content):
    for key in keys_to_check:
        if key not in content:
            return False
    return True   


def test_post__single_content(setup_test):
    client, headers = setup_test   
    response = client.post(content_url_api, json=test_contets[0], headers=headers)
    json_content = response.get_json()
    
    # Check the response code
    assert response.status_code == 201
    
    # Check if the json response contain all keys
    assert check_keys(json_content)
    
    # Check if the json is the expected
    assert equals(test_contets[0], json_content)


def test_bad_post_content(setup_test):
    client, headers = setup_test
    for bad_content in bad_contents_post:
        response = client.post(content_url_api, json=bad_content, headers=headers)
        # Check the status code
        assert response.status_code == 400
    
    # Check response without json body
    response = client.post(content_url_api, headers=headers)
    assert response.status_code == 400


def test_multiple_post(setup_test):
    client, headers = setup_test
    for content_to_test in test_contets:
        response = client.post(content_url_api, json=content_to_test, headers=headers)
        assert response.status_code == 201

    # Check if all contets are registered in the ws
    contents = Content.query.all()
    for index, content in enumerate(test_contets):
        assert equals(content, contents[index].serialize)
