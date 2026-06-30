import json
import os
from unittest.mock import patch

from django.conf import settings
import pytest
from social_core.exceptions import AuthTokenError
from social_core.tests.backends.test_azuread import AzureADTenantOAuth2Test


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
