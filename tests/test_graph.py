
from unicef_security.graph import Synchronizer


def test_token(graph_vcr):
    with graph_vcr.use_cassette('test_token.yml'):
        s = Synchronizer()
        assert s.access_token


def test_user_data(graph_vcr):
    with graph_vcr.use_cassette('test_user_data.yml'):
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
