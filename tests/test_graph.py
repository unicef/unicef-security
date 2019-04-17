import os
from pathlib import Path

import pytest

from tests.fixtures import VCR
from unicef_security.graph import Synchronizer


def default_group():
    pass

def test_get_unicef_user():
    pass

def test_get_unicef_user_doesnotexists():
    pass


class TestAzureADTenantOAuth2Ext():
    def test_user_data(self):
        pass

    def test_user_data_err(self):
        pass


class TestSynchronizer():
    @VCR.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/test_token.yml'))
    @pytest.mark.skipif(os.environ.get("CIRCLECI") == "true", reason="Skip in CirlceCI")
    def test_token(self):
        s = Synchronizer()
        assert s.access_token


    @pytest.mark.skipif(os.environ.get("CIRCLECI") == "true", reason="Skip in CirlceCI")
    @VCR.use_cassette(str(Path(__file__).parent / 'vcr_cassettes/test_user_data.yml'))
    def test_user_data(self):
        s = Synchronizer()
        info = s.get_user('sapostolico@unicef.org')
        assert info['displayName']
        assert info['givenName']
        assert info['id']
        assert sorted(info.keys()) == sorted(['@odata.context', 'id', 'businessPhones',
                                            'displayName', 'givenName', 'jobTitle',
                                            'mail', 'mobilePhone', 'officeLocation',
                                            'preferredLanguage', 'surname',
                                            'userPrincipalName'])

    def test_get_token_err(self):
        pass

    def test_delta_link(self):
        pass

    def test_delta_link_setter(self):
        pass

    def test_get_page(self):
        pass

    def test_get_page_err(self):
        pass

    def test_iterator(self):
        pass

    def test_get_record(self):
        pass

    def test_fetch_users(self):
        pass

    def test_search_users(self):
        pass

    def test_filter_users_by_email(self):
        pass

    def test_sync_user(self):
        pass

    def test_resume(self):
        pass

    def test_is_valid(self):
        pass

    def test_syncronize(self):
        pass

    def test_syncronize_err(self):
        pass
