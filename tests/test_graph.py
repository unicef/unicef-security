
import mock
import requests_mock

import pytest

from unicef_security.graph import Synchronizer, SyncResult
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


@pytest.mark.django_db
def test_search_users(graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
        class Record:
            pass

        record = Record()
        record.email = 'csaba.denes@nordlogic.com'
        record.first_name = 'csaba'
        record.last_name = 'denes'

        s = Synchronizer()
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


def test_syncresult(graph_vcr, monkeypatch):
    class SyncObj:
        def __init__(self, pk=None):
            self.pk = pk

    s = SyncResult()
    s.log(SyncObj(), True)
    s.log(SyncObj(1), False)
    s.log('random string')
    assert str(s) == '<SyncResult: 1 1 1>'

    with pytest.raises(ValueError):
        s + 'random string'

    s_new = SyncResult()
    s_new.log(SyncObj(), True)
    s_new.log(SyncObj(1), False)
    s_new.log('random string')
    assert str(s_new) == '<SyncResult: 1 1 1>'

    assert s == s_new
    assert s != 'random string'


@pytest.mark.django_db
def test_resume(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        assert User.objects.count() == 0
        s.resume(max_records=1, delta_link=s.startUrl)
        assert User.objects.count() == 2


def test_get_page(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        monkeypatch.setattr('unicef_security.graph.Synchronizer.get_token', mock.Mock(return_value=''))
        s = Synchronizer()
        with requests_mock.Mocker() as m:
            errorRsp = {"error": {"message": "random error"}}
            m.register_uri('GET', s.startUrl, json=errorRsp, status_code=401)

            with pytest.raises(ConnectionError):
                s.get_page(s.startUrl)

        with requests_mock.Mocker() as m:
            m.register_uri('GET', s.startUrl, json={}, status_code=500)

            with pytest.raises(ConnectionError):
                s.get_page(s.startUrl)


@pytest.mark.skip("TODO: figure out how to mock this")
@pytest.mark.django_db
def test_iter(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        mock_list = mock.Mock(return_value='')
        monkeypatch.setattr('unicef_security.graph.Synchronizer.get_page', mock_list)
        with pytest.raises(AttributeError):
            s.syncronize()


@pytest.mark.django_db
def test_syncronize_err(graph_vcr, monkeypatch):
    with graph_vcr.use_cassette('test_user_data.yml'):
        s = Synchronizer()
        assert User.objects.count() == 0
        s.syncronize(max_records=1)
        assert User.objects.count() == 2
        mock_err = mock.Mock(side_effect=Exception('Sync error'))
        monkeypatch.setattr('unicef_security.graph.Synchronizer.get_record', mock_err)
        with pytest.raises(Exception) as e:
            s.syncronize()
            assert e == 'Sync error'
