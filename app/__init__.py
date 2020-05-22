import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.logging import default_handler
from flask_request_id_header.middleware import RequestID
from app.resources.encoders import CustomJSONEncoder
from app.resources.logger import formatter
from flask_jwt import JWT

db = SQLAlchemy()


def create_app(config):

    from .mock_api import setup_blueprint as mock_api_blueprint
    from .new_api import setup_blueprint as new_api_blueprint

    default_handler.setFormatter(formatter)

    # create application instance
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    # config from object
    app.config.from_object(config)

    db.init_app(app)
    RequestID(app)

    from app.resources.authentication import identity, authenticate

    jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

    # repetir isso para outros modulos
    app.register_blueprint(mock_api_blueprint())
    app.register_blueprint(new_api_blueprint())

    return app
