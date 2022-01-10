from werkzeug.wrappers import response
import pytest
from test import setup_app
from app.models import content
from app.models.content import Content
from app.models.user import User
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
    client = setup_app
    user = User('test', 'passw')
    user.save()
    content_list = []
    for content_to_add in test_contents:
        content_to_add['owner'] = user
        content_to_add['node'] = None
        content = Content(**content_to_add)
        content.save()
        content_list.append(content)
    return client, content_list


def test_content_id(setup_test):
    client, content_list = setup_test
    response = client.get(content_url_api + str(content_list[0].id))
    content_json = response.get_json()
    assert equals(content_json, test_contents[0])


def test_content_bad_id(setup_test):
    client, content_list = setup_test
    response = client.get(content_url_api + str(len(content_list) + 1))
    assert response.status_code == 404


def test_search_by_title_unique(setup_test):
    client, content_list = setup_test
    response = client.get(content_url_api + f"?title={test_contents[0]['title']}")
    content_json = response.get_json()
    assert response.status_code == 200
    assert equals(test_contents[0], content_json[0])


def test_search_by_description(setup_test):
    client, content_list = setup_test
    
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
    client, _ = setup_test
    url_request = content_url_api + '?keyword={0}&value={1}'

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
    client, _ = setup_test
    url_request = content_url_api + '?title={0}&description={1}&keyword={2}&value={3}' 
    content = test_contents[3]
    keyword = content['keywords'][0]

    # Test search by multiples args
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


def test_simple_partial_search(setup_test):
    client, content_list = setup_test
    url_to_test = content_url_api + '?description=description&partial=true'
    url_to_test_not_match = content_url_api + '?description=not&partial=true'
    
    # Check multiples matchs
    response = client.get(url_to_test)
    assert response.status_code == 200
    contents_json = response.get_json()
    assert len(contents_json) == 2
    for content in contents_json:
        id = content['id'] - 1
        assert equals(content_list[id].serialize, content)

    # Check not match
    response = client.get(url_to_test_not_match)
    assert response.status_code == 200
    assert len(response.get_json()) == 0


def test_multiple_partial_search(setup_test):
    client, content_list = setup_test

    # Test with title
    url_to_test_1 = content_url_api + '?title=titlekey1&description=description&partial=true'
    # Test with keyword
    url_to_test_2 = content_url_api + '?keyword=testkey2&value=aa&description=description&partial=true'
    # Test with title and keyword 
    url_to_test_3 = content_url_api + '?title=titlekey1&keyword=testkey2&value=aa&description=description&partial=true' 

    urls_to_test = [url_to_test_1, url_to_test_2, url_to_test_3] 
    for url_to_test in urls_to_test:
        response = client.get(url_to_test_1)
        assert response.status_code == 200
        contents_json = response.get_json()
        assert len(contents_json) == 1
        id = contents_json[0]['id']
        assert equals(content_list[id - 1].serialize, contents_json[0]) 


def test_bad_partial_search(setup_test):
    client, _ = setup_test

    # Check not description arg
    response = client.get(content_url_api + '?partial=true')
    assert response.status_code == 400


def test_owner(setup_test):
    client, contents = setup_test

    for content in contents:
        response = client.get(f'{content_url_api}{content.id}/user/')
        assert response.status_code == 200
        response_json = response.get_json()
        assert 'owner' in response_json
        assert response_json['owner'] == 'test'

    
       




