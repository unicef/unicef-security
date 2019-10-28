import mock

import pytest

from unicef_security.sync import load_business_area, load_region


def test_load_business_area(db, vision_vcr):
    with vision_vcr.use_cassette('load_business_area.yml'):
        ret = load_business_area()
        assert len(ret.created) > 0
        assert len(ret.updated) == 0


def test_load_region(db, vision_vcr):
    with vision_vcr.use_cassette('load_region.yml'):
        ret = load_region()
        assert len(ret.created) == 8
        assert len(ret.updated) == 0

    with pytest.raises(PermissionError):
        mock.patch('unicef_security.sync.get_vision_auth', mock.Mock(return_value={}))
        load_region()
