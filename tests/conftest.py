import os
from pathlib import Path

from vcr import VCR

import pytest


@pytest.fixture(scope="module")
def user():
    from demo.factories import UserFactory
    return UserFactory()


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'redis://',
    }


@pytest.fixture(autouse=True)
def _check_environ(request):
    marker = request.node.get_closest_marker('skipif_missing')
    if marker:
        missing = [v for v in marker.args if v not in os.environ]
        if missing:
            pytest.skip(f"{','.join(missing)} not found in environment")


def _getvcr(request, env):
    if env in os.environ:
        params = {'record_mode': 'all'}
    else:
        params = {'record_mode': 'none'}
    path = str(Path(request.fspath).parent / 'cassettes' / str(request.function.__name__))
    return VCR(cassette_library_dir=path,
               filter_headers=['authorization', 'token'],
               filter_post_data_parameters=['client_id', 'client_secret'],
               filter_query_parameters=['access_key'],
               **params)


@pytest.fixture(scope='function')
def vision_vcr(request):
    return _getvcr(request, 'VISION_USER')


@pytest.fixture(scope='function')
def graph_vcr(request):
    return _getvcr(request, 'GRAPH_CLIENT_ID')
