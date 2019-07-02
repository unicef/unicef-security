import json

import constance
import mock
from django.contrib import messages as message_backend
from django.contrib.messages.storage import cookie
from django.urls import reverse

import pytest

from unicef_security import admin, graph
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

    # we should have an ERROR level message in the messages backend
    res.click('Sync')
    messages = _parse_messages(django_app.cookies['messages'])
    assert messages[0].level == message_backend.ERROR


@pytest.mark.django_db
def test_user_admin_sync_user_fail(django_app, admin_user, azure_user, client, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_change", args=[admin_user.id])
        res = django_app.get(url, user=admin_user)
        res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'Cannot sync user without azure_id'


def test_user_admin_sync_user(django_app, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_change", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        res.click('Sync')
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'User synchronized'


@pytest.mark.django_db
def test_user_admin_link_user_err(django_app, monkeypatch, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_link_user_data", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        form = res.forms['link_user']
        assert form.method == 'POST'

        mock_err = mock.Mock(side_effect=Exception('testing link failure'))
        monkeypatch.setattr('unicef_security.admin.Synchronizer.search_users', mock_err)
        form.submit()
        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].level == message_backend.ERROR
        assert messages[0].message == 'testing link failure'


@pytest.mark.django_db
def test_user_admin_link_user(django_app, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_link_user_data", args=[azure_user.id])
        res = django_app.get(url, user=azure_user)
        form = res.forms['link_user']
        assert form.method == 'POST'

        formres = form.submit()
        assert formres.context['message'] == 'Select one entry to link'

        form.set('selection', azure_user.azure_id)
        form.submit()

        messages = _parse_messages(django_app.cookies['messages'])
        assert messages[0].message == 'User linked'


@pytest.mark.django_db
def test_user_admin_load_admin_users(django_app, azure_user, graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        url = reverse(f"admin:unicef_security_user_load")
        res = django_app.get(url, user=azure_user)
        form = res.forms['load_users']
        assert form.method == 'POST'

        # not sure what to check here.. run it for coverage
        formres = form.submit()

        form.set('emails', 'csa')
        graph.ADMIN_EMAILS = [
            'csaba.denes@nordlogic.com',
            'csaba.denes_gmail.com#EXT#@nordlogic.onmicrosoft.com'
        ]
        formres = form.submit()

        # https://pypi.org/project/pyquery/
        syncresult = formres.pyquery(".messagelist .info").text()
        expected_syncres = (1, 1, 0)  # this depends on the results returned by Azure.
        assert syncresult == "%s users have been created,%s updated.%s invalid entries found." % expected_syncres


@pytest.mark.django_db
def test_user_admin_load_users(django_app, azure_user, graph_vcr, group):
    with graph_vcr.use_cassette('test_user_data.yml'):
        '''
        test the `load_users` flow without setting admin emails
        '''

        # create grp
        group(name=constance.config.DEFAULT_GROUP)

        url = reverse(f"admin:unicef_security_user_load")
        res = django_app.get(url, user=azure_user)
        form = res.forms['load_users']
        form.set('emails', 'csa')
        graph.ADMIN_EMAILS = []
        formres = form.submit()
        # https://pypi.org/project/pyquery/
        syncresult = formres.pyquery(".messagelist .info").text()
        expected_syncres = (1, 1, 0)  # this depends on the results returned by Azure.
        assert syncresult == "%s users have been created,%s updated.%s invalid entries found." % expected_syncres


def _parse_messages(messages_str):
    # taken from https://github.com/django/django/blob/master/django/contrib/messages/storage/cookie.py
    messages_str = messages_str.encode().decode('unicode-escape').strip('"').strip("'")
    return json.loads(messages_str.split('$')[1], cls=cookie.MessageDecoder)
