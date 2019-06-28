from django.urls import reverse

from unicef_security import admin
from unicef_security.models import User


def test_changelist(django_app, admin_user):
    url = reverse(f"admin:unicef_security_user_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_admin_reverse(django_app, admin_user):
    url = reverse(f"admin:unicef_security_user_changelist")
    assert admin.admin_reverse(User) == url


def test_region_admin_sync(django_app, admin_user, vision_vcr):
    url = reverse(f"admin:unicef_security_region_changelist")
    res = django_app.get(url, user=admin_user)
    with vision_vcr.use_cassette('load_region.yaml'):
        res.click('Sync')


def test_business_area_admin_sync(django_app, admin_user, vision_vcr):
    url = reverse(f"admin:unicef_security_businessarea_changelist")
    res = django_app.get(url, user=admin_user)
    with vision_vcr.use_cassette('business_area.yaml'):
        res.click('Sync')
