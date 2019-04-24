from tests import factories

import pytest


@pytest.fixture(scope="module")
def user():
    return factories.UserFactory()


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'redis://',
        # CELERY_TASK_ALWAYS_EAGER: True,
        # CELERY_ALWAYS_EAGER: True,
        # 'task_always_eager': True,
    }
