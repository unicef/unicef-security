import mock

import pytest


@pytest.mark.usefixtures('depends_on_current_app')
def test_sync_business_area(monkeypatch):
    # importing `sync_business_area` before the celery fixture is loaded results in error
    from unicef_security.tasks import sync_business_area

    mock_business_area = mock.Mock()
    monkeypatch.setattr('unicef_security.tasks.load_business_area', mock_business_area)
    with pytest.raises(AssertionError):
        mock_business_area.assert_called_with()
    sync_business_area.apply()
    mock_business_area.assert_called_with()
