
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
