import flask
import flask_praetorian

from extensions import guard


def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token containing additional custom claims.

    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = flask.request.get_json(force=True)
    username = req.pop('username', None)
    password = req.pop('password', None)
    user = guard.authenticate(username, password)
    return flask.jsonify(access_token=guard.encode_jwt_token(
        user,
        firstname=user.firstname,
        nickname=user.nickname,
        surname=user.surname,
    ))


@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT

    .. example::
       $ curl http://localhost:5000/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    custom_claims = flask_praetorian.current_custom_claims()
    firstname = custom_claims.pop('firstname', None)
    nickname = custom_claims.pop('nickname', None)
    surname = custom_claims.pop('surname', None)

    if nickname is None:
        user_string = "{} {}".format(firstname, surname)
    else:
        user_string = "{} '{}' {}".format(firstname, nickname, surname)

    return flask.jsonify(
        message="protected endpoint (allowed user {u})".format(u=user_string),
    )


def register_routes(app):
    app.add_url_rule(
        '/login',
        view_func=login,
        methods=['POST'],
    )
    app.add_url_rule(
        '/protected',
        view_func=protected,
    )
