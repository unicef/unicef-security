import pytest

from unicef_security.templatetags.security import ad_backend, settings_value


@pytest.mark.parametrize(
    "key,value", (["LANGUAGE_CODE", "en-us"], ["AUTH_USER_MODEL", "demo.User"])
)
def test_settings_value(key, value):
    assert settings_value(key) == value


def test_ad_backend():
    assert ad_backend() == "/social/login/azuread-tenant-oauth2/"
