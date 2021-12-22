import os
from .config import app_config, BASE_URL
from flask import Flask, jsonify, request
from flask_migrate import Migrate, migrate
from .models import db
from .controllers.content_controller import content_controller

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config[os.environ['APP_SETTINGS']])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # Registry the controllers
    app.register_blueprint(content_controller, url_prefix='/content/')

    @app.route('/')
    def api_welcome():
        return '<h1>MyTube API</h1>'
            
    return app
