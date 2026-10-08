import json
import os
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import authenticate
import pytest
from social_core.exceptions import AuthTokenError
from social_core.tests.backends.test_azuread import AzureADTenantOAuth2Test

from .factories import SuperUserFactory, UserFactory


class UNICEFAzureADTenantOAuth2ExtTest(AzureADTenantOAuth2Test):
    backend_path = "unicef_security.backends.UNICEFAzureADTenantOAuth2Ext"

    def test_login_unverified(self) -> None:
        with patch.dict(os.environ, {"OAUTH2_VERIFY": "False"}):
            self.do_login()

    def test_login_unverified_malformed_token(self) -> None:
        self.access_token_body = json.dumps(
            {
                "access_token": "foobar",
                "token_type": "bearer",
                "id_token": "completely-malformed-token",
            }
        )
        with patch.dict(os.environ, {"OAUTH2_VERIFY": "False"}):
            with pytest.raises(AuthTokenError):
                self.do_start()

    def test_login_unverified_dev_default(self) -> None:
        environ = os.environ.copy()
        environ.pop("OAUTH2_VERIFY", None)
        with patch.dict(os.environ, environ, clear=True):
            with patch.object(settings, "DEBUG", True):
                self.do_login()


@pytest.mark.django_db
def test_superuser_can_authenticate() -> None:
    user = SuperUserFactory()
    assert authenticate(username=user.username, password="password") == user


@pytest.mark.django_db
def test_staff_only_user_cannot_authenticate() -> None:
    user = UserFactory(is_staff=True)
    assert authenticate(username=user.username, password="password") is None


@pytest.mark.django_db
def test_superuser_without_staff_cannot_authenticate() -> None:
    user = UserFactory(is_superuser=True, is_staff=False)
    assert authenticate(username=user.username, password="password") is None


@pytest.mark.django_db
def test_superuser_and_staff_can_authenticate() -> None:
    user = UserFactory(is_superuser=True, is_staff=True)
    assert authenticate(username=user.username, password="password") == user


@pytest.mark.django_db
def test_regular_user_cannot_authenticate() -> None:
    user = UserFactory()
    assert authenticate(username=user.username, password="password") is None


@pytest.mark.django_db
def test_wrong_password_cannot_authenticate() -> None:
    user = SuperUserFactory()
    assert authenticate(username=user.username, password="invalid") is None
