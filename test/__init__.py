import pytest
from app import create_app
from app.models import db

@pytest.fixture
def setup_app():
    # Create app
    app = create_app(app_settings='testing')
    db.init_app(app)

    with app.app_context():
        # Add contents
        db.create_all()
        content_list = []
        yield app
        # Remove contents
        db.session.remove()
        db.drop_all()
