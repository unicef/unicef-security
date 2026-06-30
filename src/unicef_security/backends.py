import os

import jwt
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.exceptions import AuthTokenError


class UNICEFAzureADTenantOAuth2Ext(AzureADTenantOAuth2):
    name = "unicef-azuread-tenant-oauth2"

    def user_data(self, access_token, *args, **kwargs):
        verify = os.environ.get("OAUTH2_VERIFY", "").lower() in ("true", "1", "yes")
        if verify:
            return super().user_data(access_token, *args, **kwargs)

        response = kwargs.get("response") or {}
        id_token = response.get("id_token") or access_token
        try:
            return jwt.decode(
                id_token,
                options={"verify_signature": False},
            )
        except jwt.PyJWTError as error:
            raise AuthTokenError(self, error)
