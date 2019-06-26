import json
import mock
import uuid

# from django.conf import settings
# from django.contrib.messages import get_messages
from django.contrib import messages as message_backend
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

    # test sync failure. we should have an ERROR level message in the messages backend
    res.click('Sync')
    messages = _parse_messages(django_app.cookies['messages'])
    assert messages[0].level == message_backend.ERROR


# @pytest.mark.skip(reason="")
@pytest.mark.django_db
def test_user_admin_sync_user_fail(django_app, admin_user, azure_user, client, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_change", args=[admin_user.id])
        res = django_app.get(url, user=admin_user)
        response = res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'Cannot sync user without azure_id'


def test_user_admin_sync_user(django_app, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_change", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        response = res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'User synchronized'


@pytest.mark.django_db
def test_user_admin_link_user_err(django_app, monkeypatch, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_link_user_data", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        form = res.forms[0]
        assert form.action == '' and form.method == 'POST'
        mock_err = mock.Mock(side_effect=Exception('testing link fail'))
        monkeypatch.setattr('unicef_security.admin.Synchronizer.search_users', mock_err)
        formres = form.submit()
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].level == message_backend.ERROR
        assert messages[0].message == 'testing link failure'


# @pytest.mark.skip(reason="")
@pytest.mark.django_db
def test_user_admin_link_user(django_app, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_link_user_data", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        form = res.forms[0]
        assert form.action == '' 
        assert form.method == 'POST'

        formres = form.submit()
        assert formres.context['message'] == 'Select one entry to link'
        
        form.set('selection', azure_user.azure_id)
        formres = form.submit()
        
        # if 'messages' in django_app.cookies:
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'User linked'


def _parse_messages(messages_str):
    # taken from https://github.com/django/django/blob/master/django/contrib/messages/storage/cookie.py
    messages_str = messages_str.encode().decode('unicode-escape').strip('"').strip("'")
    return json.loads(messages_str.split('$')[1], cls=cookie.MessageDecoder)
