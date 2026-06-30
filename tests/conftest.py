import sys
from pathlib import Path

import pytest
import responses
import os

from .factories import UserFactory, SuperUserFactory


here = Path(__file__).parent
DEMOAPP_PATH = here / "demoapp"
sys.path.insert(0, str(here / "../src"))
sys.path.insert(0, str(DEMOAPP_PATH))


def pytest_configure(config):
    os.environ["DEBUG"] = "False"
    os.environ["OAUTH2_VERIFY"] = "True"
    os.environ.update(DJANGO_SETTINGS_MODULE="demo.settings")

    import django  # noqa

    django.setup()


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
