import flask
import flask_praetorian

from users import User
from extensions import guard, db

from basic import login, protected
from refresh import refresh, disable_user


def register():
    """
    Registers a new by parsing a POST request containing new user info and
    dispatching an email with a registration token

    .. example::
       $ curl http://localhost:5000/register -X POST \
         -d '{
           "username":"Brandt", \
           "password":"herlifewasinyourhands" \
           "email":"brandt@biglebowski.com"
         }'
    """
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    email = req.get('email', None)
    password = req.get('password', None)
    new_user = User(
        username=username,
        password=guard.hash_password(password),
        roles='operator',
    )
    db.session.add(new_user)
    guard.send_registration_email(email, user=new_user)
    ret = {'message': 'successfully sent registration email to user {}'.format(
        new_user.username
    )}
    return flask.jsonify(ret)


def finalize():
    """
    Finalizes a user registration with the token that they were issued in their
    registration email

    .. example::
       $ curl http://localhost:5000/finalize -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    registration_token = guard.read_token_from_header()
    user = guard.get_user_from_registration_token(registration_token)
    # perform 'activation' of user here...like setting 'active' or something
    ret = {'access_token': guard.encode_jwt_token(user)}
    return flask.jsonify(ret), 200


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
    app.add_url_rule(
        '/register',
        view_func=register,
        methods=['POST'],
    )
    app.add_url_rule(
        '/finalize',
        view_func=finalize,
    )
