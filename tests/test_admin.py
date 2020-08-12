from django.urls import reverse


def test_changelist(django_app, admin_user):
    url = reverse("admin:unicef_security_user_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200
