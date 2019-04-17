import mock
import pytest
import vcr

VCR = vcr.VCR(serializer='yaml',
              record_mode='once',
              match_on=['uri', 'method'],
              filter_headers=['authorization', 'token'],
              filter_post_data_parameters=['client_id', 'client_secret'])

# @pytest.fixture
# def mock_task():
#     return mock.Mock()
