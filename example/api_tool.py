import flask
import logging
import os


def basic():
    return flask.render_template(
        'basic.html',
        scripts=os.listdir(flask.current_app.static_folder),
        api_port=5000,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


def refresh():
    return flask.render_template(
        'refresh.html',
        scripts=os.listdir(flask.current_app.static_folder),
        api_port=5010,
        access_lifespan=30,
        refresh_lifespan=2*60,
    )


def blacklist():
    return flask.render_template(
        'blacklist.html',
        scripts=os.listdir(flask.current_app.static_folder),
        api_port=5020,
        access_lifespan=10000*24*60*60,
        refresh_lifespan=10000*24*60*60,
    )


def custom():
    return flask.render_template(
        'custom.html',
        scripts=os.listdir(flask.current_app.static_folder),
        api_port=5030,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


def register():
    return flask.render_template(
        'register.html',
        scripts=os.listdir(flask.current_app.static_folder),
        api_port=5040,
        access_lifespan=24*60*60,
        refresh_lifespan=30*24*60*60,
    )


def create_app():
    """
    Use the app factory pattern to create a flask app for the api tool
    """
    app = flask.Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'top secret'
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

    log_file = os.environ.get('EXAMPLE_LOG')
    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
        app.logger.info("logging to {log_file}".format(log_file=log_file))

    app.add_url_rule('/', view_func=basic)
    app.add_url_rule('/basic', view_func=basic)
    app.add_url_rule('/refresh', view_func=refresh)
    app.add_url_rule('/blacklist', view_func=blacklist)
    app.add_url_rule('/custom', view_func=custom)
    app.add_url_rule('/register', view_func=register)

    return app
