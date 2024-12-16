import responses

import pytest

from .factories import UserFactory


@pytest.fixture()
def mocked_responses():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture()
def auth_user():
    return UserFactory()
