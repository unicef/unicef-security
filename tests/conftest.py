import os
# import uuid
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
        # params = {'record_mode': 'new_episodes'}
        # params = {'record_mode': 'none'}
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


@pytest.fixture(scope='function')
def azure_user(django_user_model, django_app):
    '''
    The tests won't work without a valid Azure user
    '''
    user, _status = django_user_model.objects.get_or_create(
        username=os.environ.get('TEST_GRAPH_USER_EMAIL', 'csaba.denes@nordlogic.com'),
        azure_id=os.environ.get('TEST_GRAPH_USER_AZURE_ID', 'e02822f9-c473-4c77-9343-1c8e6c062f5e'),
        is_superuser=True,
        is_staff=True,
    )
    return user