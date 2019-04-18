# import celery
import mock
import pytest

# from celery.contrib.pytest import celery_app
# from django.test.utils import override_settings
# from unicef_security.tasks import sync_business_area

# @mock.patch('celery.app.default_app.task')
# @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# @override_settings(CELERY_ALWAYS_EAGER=True)
# def test_sync_business_area(celery_worker, monkeypatch):
# @pytest.mark.skip(reason="maybe figure out how to `delay` the task..")
@pytest.mark.usefixtures('depends_on_current_app')
def test_sync_business_area(monkeypatch):
    '''
    with celery_app.conf.update(CELERY_ALWAYS_EAGER=True):
        monkeypatch.setitem('celery.app.default_app', 'task', lambda: a)
        monkeypatch.setattr('celery.app.default_app', 'task', lambda: a, raising=False)
        monkeypatch.setattr('default_app', 'task', lambda: a)
    '''

    # sync_business_area.delay()

    # importing this at top results with error, it needs some of the lib fixtures loaded
    from unicef_security.tasks import sync_business_area
    mock_load_ba = mock.Mock()
    monkeypatch.setattr('unicef_security.tasks.load_business_area', mock_load_ba)
    with pytest.raises(AssertionError):
        mock_load_ba.assert_called_with()
    sync_business_area()
    mock_load_ba.assert_called_with()
