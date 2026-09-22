import pytest
from django.urls import reverse


def test_unicef_logout(django_app):
    resp = django_app.get(reverse("security:unicef-logout"))
    assert resp.status_code == 302


@pytest.mark.django_db
def test_unicef_logout_flushes_session(client, auth_user):
    client.force_login(auth_user)
    assert "_auth_user_id" in client.session
    client.get(reverse("security:unicef-logout"))
    assert "_auth_user_id" not in client.session


def test_unauthorized(django_app):
    resp = django_app.get(reverse("security:unauthorized"))
    assert resp.status_code == 200


def test_admin_login(django_app):
    resp = django_app.get(reverse("admin:login"))
    assert resp.status_code == 200
    assert 'method="post"' in resp.text.lower()
    assert "csrfmiddlewaretoken" in resp.text
    assert "Login with Azure" in resp.text
