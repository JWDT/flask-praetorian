import flask
import flask_praetorian

from extensions import guard
from basic import login, protected

blacklist = set()


def is_blacklisted(jti):
    return jti in blacklist


@flask_praetorian.auth_required
@flask_praetorian.roles_required('admin')
def blacklist_token():
    """
    Blacklists an existing JWT by registering its jti claim in the blacklist.

    .. example::
       $ curl http://localhost:5000/blacklist_token -X POST \
         -d '{"token":"<your_token>"}'
    """
    req = flask.request.get_json(force=True)
    data = guard.extract_jwt_token(req['token'])
    blacklist.add(data['jti'])
    return flask.jsonify(message='token blacklisted ({})'.format(req['token']))


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
    app.add_url_rule(
        '/blacklist_token',
        view_func=blacklist_token,
        methods=['POST'],
    )
