from app import create_app
from . import content_url_api

test_contets = [
    {'title':'title1', 'description': 'description1'},   
    {'title':'title2', 'description': 'description2'}
]

bad_contents_post = [
    {'tile':'not description post'},
    {'description': 'post without tile'},
    {}
]

keys_to_check = ['title', 'description', 'keywords']

def equals(content_1, content_2):
    if content_1['title'] != content_2['title']:
        return False
    elif content_1['description'] != content_2['description']:
        return False
    return True

def check_keys(content):
    for key in keys_to_check:
        if key not in content:
            return False
    return True

def test_post__single_content():
    app = create_app(app_settings='testing')
    with app.test_client() as client:
        response = client.post(content_url_api, json=test_contets[0])
        json_content = response.get_json()
        # Check the response code
        assert response.status_code == 200
        # Check if the json response contain all keys
        assert check_keys(json_content)
        # Check if the json is the expected
        assert equals(test_contets[0], json_content)

def test_bad_post_content():
    app = create_app(app_settings='testing')
    with app.test_client() as client:
        for bad_content in bad_contents_post:
            response = client.post(content_url_api, json=bad_content)
            # Check the status code
            assert response.status_code == 400

def test_multiple_post():
    app = create_app(app_settings='testing')
    with app.test_client() as client:
        pass