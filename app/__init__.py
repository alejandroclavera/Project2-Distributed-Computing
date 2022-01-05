import os
from .config import app_config, BASE_URL
from flask import Flask, jsonify, request
from flask_migrate import Migrate, migrate
from .models import db
from .controllers.content_controller import content_controller
from .controllers.user_controller import user_controller

migrate = Migrate()

def create_app(app_settings=None):
    app = Flask(__name__)

    # Load configurations
    if not app_settings:
        app.config.from_object(app_config[os.environ['APP_SETTINGS']])
    else:
        app.config.from_object(app_config[app_settings])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init the flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Registry the controllers
    app.register_blueprint(content_controller, url_prefix='/content/')
    app.register_blueprint(user_controller, url_prefix='/user/')

    @app.errorhandler(Exception)
    def error_handler(e):
        return jsonify({'error': 'server error'}), 500

    @app.route('/')
    def api_welcome():
        return '<h1>MyTube API</h1>'
            
    return app
