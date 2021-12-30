import pytest
from test import setup_app
from app.models import content
from app.models.content import Content
from app.models import db
from . import content_url_api

###################################
#   TEST get content information  #
###################################
test_contents = [
    {'title': 'title1', 'description': 'title2'},
    {'title': 'title2', 'description': 'title2'},
    {'title': 'titlekey1', 'description':'descriptionkey', 'keywords':[
        {'keyword':'testkey1', 'value':'32'}, 
        {'keyword': 'testkey2', 'value': 'aa'}
    ]},
     {'title': 'titlekey2', 'description':'descriptionkey2', 'keywords':[
        {'keyword':'testkey1', 'value':'32'}, 
    ]},
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
    content_list = []
    for content_to_add in test_contents:
        content = Content(*content_to_add.values())
        content.save()
        content_list.append(content)
    return app, content_list


def test_content_id(setup_test):
    app, content_list = setup_test
    with app.test_client() as client:
        response = client.get(content_url_api + str(content_list[0].id))
        content_json = response.get_json()
        assert equals(content_json, test_contents[0])


def test_content_bad_id(setup_test):
    app, content_list = setup_test
    with app.test_client() as client:
        response = client.get(content_url_api + str(len(content_list) + 1))
        assert response.status_code == 404


def test_search_by_title_unique(setup_test):
    app, content_list = setup_test
    with app.test_client() as client:
        response = client.get(content_url_api + f"?title={test_contents[0]['title']}")
        content_json = response.get_json()
        assert response.status_code == 200
        assert equals(test_contents[0], content_json[0])


def test_search_by_description(setup_test):
    app, content_list = setup_test
    with app.test_client() as client:
        # Test arrived one result
        response = client.get(content_url_api + f"?description={test_contents[2]['description']}")
        assert response.status_code == 200
        single_content_json = response.get_json()
        assert len(single_content_json) == 1
        assert equals(test_contents[2], single_content_json[0])

        # Test mulitples results
        response = client.get(content_url_api + f"?description={test_contents[0]['description']}")
        assert response.status_code == 200
        multiple_content_json = response.get_json()
        assert len(multiple_content_json) == 2
        assert equals(test_contents[0], multiple_content_json[0]) 
        assert equals(test_contents[1], multiple_content_json[1])


def test_search_by_keywords(setup_test):
    app, _ = setup_test
    url_request = content_url_api + '?keyword={0}&value={1}'
    with app.test_client() as client:
        # Test one result
        unique_keyword = test_contents[2]['keywords'][1]
        response = client.get(url_request.format(unique_keyword['keyword'], unique_keyword['value']))
        assert response.status_code == 200
        content_json = response.get_json()
        assert len(content_json) == 1
        assert equals(test_contents[2], content_json[0]) 

        # Test multiples results
        unique_keyword = test_contents[2]['keywords'][0]
        response = client.get(url_request.format(unique_keyword['keyword'], unique_keyword['value']))
        assert response.status_code == 200
        content_json = response.get_json()
        assert len(content_json) == 2
        assert equals(test_contents[2], content_json[0])
        assert equals(test_contents[3], content_json[1])  

def test_multiple_search(setup_test):
    app, _ = setup_test
    url_request = content_url_api + '?title={0}&description={1}&keyword={2}&value={3}' 
    content = test_contents[3]
    keyword = content['keywords'][0]
    with app.test_client() as client:
        response = client.get(url_request.format(content['title'], content['description'], keyword['keyword'], keyword['value']))
        assert response.status_code == 200
        content_json = response.get_json()
        print(content_json)
        assert len(content_json) == 1
        assert equals(content, content_json[0])
        # Search not match
        response = client.get(url_request.format('not found title', 'not_found description', '', ''))
        assert response.status_code == 200
        assert len(response.get_json()) == 0