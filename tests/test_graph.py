
import mock

import pytest

from unicef_security.graph import Synchronizer
from unicef_security.models import User


def test_token(graph_vcr):
    with graph_vcr.use_cassette('test_token.yml'):
        s = Synchronizer()
        assert s.access_token


def test_user_data(graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        info = s.get_user('sapostolico@unicef.org')
        assert info['displayName']
        assert info['givenName']  # it seems some users have this field empty
        assert info['id']
        assert sorted(info.keys()) == sorted(['@odata.context', 'id', 'businessPhones',
                                              'displayName', 'givenName', 'jobTitle',
                                              'mail', 'mobilePhone', 'officeLocation',
                                              'preferredLanguage', 'surname',
                                              'userPrincipalName'])


def test_get_user_by_token(graph_vcr):
    '''
    this looks to be a middleware method, not sure how to test this
    '''
    pass


def test_get_unicef_user(graph_vcr):
    '''
    this method seems to use non-existent model fields, not sure how to test this
    '''
    pass


@pytest.mark.skip("TODO: fix")
@pytest.mark.django_db
def test_search_users(graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        record = {
            'email': 'csaba.denes@nordlogic.com',
            'last_name': 'csaba',
            'first_name': 'denes',
        }
        res = s.search_users(record)
        assert res


@pytest.mark.django_db
def test_filter_users_by_email(graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        email = 'csaba.denes@nordlogic.com'
        res = s.filter_users_by_email(email)
        if len(res) > 0:
            assert res[0]['mail'] == email or res[0]['userPrincipalName'] == email


@pytest.mark.django_db
def test_resume(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        assert User.objects.count() == 0
        s.resume(max_records=1, delta_link=s.startUrl)
        assert User.objects.count() == 2


@pytest.mark.django_db
def test_syncronize_err(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        assert User.objects.count() == 0
        s.syncronize(max_records=1)
        assert User.objects.count() == 2
        mock_err = mock.Mock(side_effect=Exception('Sync error'))
        monkeypatch.setattr('unicef_security.admin.Synchronizer.get_record', mock_err)
        with pytest.raises(Exception) as e:
            s.syncronize()
            assert e == 'Sync error'
