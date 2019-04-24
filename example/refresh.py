import flask
import flask_praetorian

from extensions import guard, db
from users import User
from basic import login, protected


def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.

    .. example::
       $ curl http://localhost:5000/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    old_token = guard.read_token_from_header()
    new_token = guard.refresh_jwt_token(old_token)
    return flask.jsonify(access_token=new_token)


@flask_praetorian.auth_required
@flask_praetorian.roles_required('admin')
def disable_user():
    """
    Disables a user in the data store

    .. example::
        $ curl http://localhost:5000/disable_user -X POST \
          -H "Authorization: Bearer <your_token>" \
          -d '{"username":"Walter"}'
    """
    req = flask.request.get_json(force=True)
    usr = User.query.filter_by(username=req.get('username', None)).one()
    usr.is_active = False
    db.session.commit()
    return flask.jsonify(message='disabled user {}'.format(usr.username))


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
        '/refresh',
        view_func=refresh,
    )
    app.add_url_rule(
        '/disable_user',
        view_func=disable_user,
        methods=['POST'],
    )
