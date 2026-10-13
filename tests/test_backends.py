import os
from unittest.mock import patch

import pytest
from django.contrib.auth import authenticate
from jwt import DecodeError
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.exceptions import AuthResponseError

from unicef_security.backends import UNICEFAzureADTenantOAuth2Ext

from .factories import SuperUserFactory, UserFactory


@patch("unicef_security.backends.jwt.decode")
def test_user_data_unverified_decode_token(mock_decode):
    mock_decode.return_value = {"sub": "123", "email": "test@example.com"}
    with patch.dict(os.environ, {"OAUTH2_VERIFY": "False"}):
        result = UNICEFAzureADTenantOAuth2Ext().user_data("access-token", response={"id_token": "the-id-token"})
    assert result == {"sub": "123", "email": "test@example.com"}
    mock_decode.assert_called_once_with("the-id-token", options={"verify_signature": False})


@patch("unicef_security.backends.jwt.decode")
def test_user_data_unverified_malformed_token_raises(mock_decode):
    mock_decode.side_effect = DecodeError("Invalid header padding")
    with patch.dict(os.environ, {"OAUTH2_VERIFY": "False"}):
        with pytest.raises(AuthResponseError):
            UNICEFAzureADTenantOAuth2Ext().user_data(
                "access-token", response={"id_token": "completely-malformed-token"}
            )


@patch("unicef_security.backends.jwt.decode")
def test_user_data_dev_default_disables_verification(mock_decode, settings):
    mock_decode.return_value = {"sub": "123"}
    environ = os.environ.copy()
    environ.pop("OAUTH2_VERIFY", None)
    with patch.dict(os.environ, environ, clear=True):
        settings.DEBUG = True
        result = UNICEFAzureADTenantOAuth2Ext().user_data("the-id-token")
    assert result == {"sub": "123"}
    mock_decode.assert_called_once()


@patch.object(AzureADTenantOAuth2, "user_data")
def test_user_data_verify_passes_through_to_base(mock_user_data):
    mock_user_data.return_value = {"sub": "123"}
    with patch.dict(os.environ, {"OAUTH2_VERIFY": "true"}):
        result = UNICEFAzureADTenantOAuth2Ext().user_data("access-token", response={"id_token": "the-id-token"})
    assert result == {"sub": "123"}
    mock_user_data.assert_called_once_with("access-token", response={"id_token": "the-id-token"})


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
