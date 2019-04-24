import flask
import importlib
import logging
import os
import pendulum
import tempfile

from extensions import guard, db, cors
from users import User


def fetch_env(app, key, default=None):
    app.config[key] = os.environ.get(key, default)


def create_app(config_file=None):
    """
    Use the app factory pattern to create a flask app for the example
    """
    app = flask.Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'top secret'
    fetch_env(app, 'JWT_ACCESS_LIFESPAN', default=pendulum.duration(hours=24))
    fetch_env(app, 'JWT_REFRESH_LIFESPAN', default=pendulum.duration(days=30))
    fetch_env(app, 'PRAETORIAN_CONFIRMATION_SENDER')
    fetch_env(app, 'PRAETORIAN_CONFIRMATION_SUBJECT')
    fetch_env(app, 'MAIL_SERVER')

    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User)

    # Initialize a local database for the example
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
        tempfile.NamedTemporaryFile(prefix='local', suffix='.db')
    )
    db.init_app(app)

    # Initializes CORS so that the api_tool can talk to the example app
    cors.init_app(app)

    # Add in the users
    User.create_users(app)

    log_file = os.environ.get('EXAMPLE_LOG')
    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

    routes = importlib.import_module(os.environ['EXAMPLE'])
    routes.register_routes(app)

    return app
