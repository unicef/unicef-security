import os

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
import jwt
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.exceptions import AuthTokenError


class UNICEFAzureADTenantOAuth2Ext(AzureADTenantOAuth2):
    name = "unicef-azuread-tenant-oauth2"

    def user_data(self, access_token, *args, **kwargs):
        if "OAUTH2_VERIFY" in os.environ:
            verify = os.environ["OAUTH2_VERIFY"].lower() in ("true", "1", "yes")
        else:
            verify = not getattr(settings, "DEBUG", False)

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


class SuperuserModelBackend(ModelBackend):
    """Allow database (username/password) login only to staff and superusers."""

    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user) and (user.is_staff or user.is_superuser)
