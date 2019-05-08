import json
import uuid

# from django.conf import settings
# from django.contrib.messages import get_messages
from django.contrib.messages.storage import cookie
# from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse

import pytest

from unicef_security import admin
# from unicef_security.graph import Synchronizer
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


@pytest.mark.django_db
def test_user_admin_sync_user(django_app, admin_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        user = User(username='test_1')
        user.save()
        url = reverse(f"admin:unicef_security_user_change", args=[user.id])
        res = django_app.get(url, user=admin_user)
        response = res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'Cannot sync user without azure_id'

        user = User(username='test_2', azure_id = uuid.uuid4())
        user.save()
        url = reverse(f"admin:unicef_security_user_change", args=[user.id])
        res = django_app.get(url, user=admin_user)
        response = res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        # TODO: fix casette issue..
        # assert messages[0].message == 'User synchronized'

def _parse_messages(messages_str):
    # taken from https://github.com/django/django/blob/master/django/contrib/messages/storage/cookie.py
    messages_str = messages_str.encode().decode('unicode-escape').strip('"').strip("'")
    return json.loads(messages_str.split('$')[1], cls=cookie.MessageDecoder)
