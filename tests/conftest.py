import responses

import pytest

from .factories import UserFactory, SuperUserFactory


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def auth_user():
    return UserFactory()


@pytest.fixture
def app(django_app_factory, mocked_responses):
    django_app = django_app_factory(csrf_checks=False)
    admin_user = SuperUserFactory(username="superuser")
    django_app.set_user(admin_user)
    django_app._user = admin_user
    return django_app
