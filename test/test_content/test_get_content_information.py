import pytest
from app import create_app
from app.models.content import Content
from app.models import db
from . import content_url_api

##############################
#   TEST GET SINGLE CONTENT  #
##############################
test_contents = [
    {'title': 'title1', 'description': 'title2'},
    {'title': 'title2', 'description': 'title2'},
]


def equals(content_1, content_2):
    if content_1['title'] != content_2['title']:
        return False
    elif content_1['description'] != content_2['description']:
        return False
    return True


@pytest.fixture
def setup_test():
    # Create app
    app = create_app(app_settings='testing')
    db.init_app(app)

    with app.app_context():
        # Add contents
        db.create_all()
        content_list = []
        for content_to_add in test_contents:
            content = Content(*content_to_add.values())
            content.save()
            content_list.append(content)
        yield app, content_list
        # Remove contents
        db.session.remove()
        db.drop_all()

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
        response = client.get(content_url_api + f'?title={test_contents[0]["title"]}')
        content_json = response.get_json()
        assert response.status_code == 200
        assert equals(test_contents[0], content_json[0])