# import celery
import mock
import pytest

from celery.contrib.pytest import celery_app
from django.test.utils import override_settings
# from unicef_security.tasks import sync_business_area

# @mock.patch('celery.app.default_app.task')
# @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# @override_settings(CELERY_ALWAYS_EAGER=True)
# def test_sync_business_area(celery_worker, monkeypatch):
# @pytest.mark.skip(reason="figure this out.. now it just blocks..")
@pytest.mark.usefixtures('depends_on_current_app')
def test_sync_business_area(monkeypatch):
    # with celery_app.conf.update(CELERY_ALWAYS_EAGER=True):
        # monkeypatch.setitem('celery.app.default_app', 'task', lambda: a)
        # monkeypatch.setattr('celery.app.default_app', 'task', lambda: a, raising=False)
        # monkeypatch.setattr('default_app', 'task', lambda: a)

    # sync_business_area.delay()

    mf_1 = mock.Mock()

    from unicef_security.tasks import sync_business_area
    monkeypatch.setattr('unicef_security.tasks.load_business_area', mf_1)
    with pytest.raises(AssertionError):
        mf_1.assert_called_with()
    sync_business_area()
    mf_1.assert_called_with()
