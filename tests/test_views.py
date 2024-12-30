from django.urls import reverse


def test_unicef_logout(django_app):
    resp = django_app.get(reverse("security:unicef-logout"))
    assert resp.status_code == 302


def test_unauthorized(django_app):
    resp = django_app.get(reverse("security:unauthorized"))
    assert resp.status_code == 200
