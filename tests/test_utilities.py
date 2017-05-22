import pytest

from flask_praetorian.utilities import (
    add_jwt_data_to_app_context,
    current_user,
    current_rolenames,
)
from flask_praetorian.exceptions import PraetorianError


class TestPraetorianUtilities:

    def test_current_user(self, user_class, db, default_guard):
        jwt_data = {}
        add_jwt_data_to_app_context(jwt_data)
        with pytest.raises(PraetorianError) as err_info:
            current_user()
        assert 'Could not fetch an id' in str(err_info.value)

        jwt_data = {'id': 31}
        add_jwt_data_to_app_context(jwt_data)
        with pytest.raises(PraetorianError) as err_info:
            current_user()
        assert 'Could not identify the current user' in str(err_info.value)

        the_dude = user_class(
            id=13,
            username='TheDude',
        )
        db.session.add(the_dude)
        db.session.commit()
        jwt_data = {'id': 13}
        add_jwt_data_to_app_context(jwt_data)
        assert current_user() is the_dude

    def test_current_rolenames(self, user_class, db, default_guard):
        jwt_data = {}
        add_jwt_data_to_app_context(jwt_data)
        assert current_rolenames() == set([
            'non-empty-but-definitely-not-matching-subset'
        ])

        jwt_data = {'rls': 'admin,operator'}
        add_jwt_data_to_app_context(jwt_data)
        assert current_rolenames() == set(['admin', 'operator'])