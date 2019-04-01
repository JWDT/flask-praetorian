import flask
import flask_praetorian

from extensions import guard


def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.

    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return (flask.jsonify(ret), 200)


@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT

    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return flask.jsonify(message='protected endpoint (allowed user {})'.format(
        flask_praetorian.current_user().username,
    ))


@flask_praetorian.roles_required('admin')
def protected_admin_required():
    """
    A protected endpoint that requires a role. The roles_required decorator
    will require that the supplied JWT includes the required roles

    .. example::
       $ curl http://localhost:5000/protected_admin_required -X GET \
          -H "Authorization: Bearer <your_token>"
    """
    return flask.jsonify(
        message='protected_admin_required endpoint (allowed user {})'.format(
            flask_praetorian.current_user().username,
        )
    )


@flask_praetorian.roles_accepted('operator', 'admin')
def protected_operator_accepted():
    """
    A protected endpoint that accepts any of the listed roles. The
    roles_accepted decorator will require that the supplied JWT includes at
    least one of th accepted roles

    .. example::
       $ curl http://localhost/protected_operator_accepted -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return flask.jsonify(
        message='protected_operator_accepted endpoint (allowed usr {})'.format(
            flask_praetorian.current_user().username,
        )
    )


def register_routes(app):
    app.add_url_rule(
        '/protected_operator_accepted',
        view_func=protected_operator_accepted,
    )
    app.add_url_rule(
        '/protected_admin_required',
        view_func=protected_admin_required,
    )
    app.add_url_rule(
        '/login',
        view_func=login,
        methods=['POST'],
    )
    app.add_url_rule(
        '/protected',
        view_func=protected,
    )
