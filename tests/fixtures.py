import mock
import vcr

VCR = vcr.VCR(serializer='yaml',
              record_mode='once',
              match_on=['uri', 'method'],
              filter_headers=['authorization', 'token'],
              filter_post_data_parameters=['client_id', 'client_secret'])


def patch_admin_extra_urls_decorators():
    mock.patch('admin_extra_urls.extras.link', lambda: None).start()
    mock.patch('admin_extra_urls.extras.action', lambda: None).start()
    mock.patch('admin_extra_urls.extras.ExtraUrlMixin', lambda: None).start()
