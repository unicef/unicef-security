import mock
import os
import pytest
import requests

from django.contrib.admin.sites import AdminSite
from django.urls import reverse

from unicef_security import admin
from unicef_security.models import User, Region


def test_admin_reverse():
    model = User
    page="changelist"
    reversed = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}")
    assert reversed == admin.admin_reverse(User)

def test_region_admin_sync(monkeypatch, requests_mock):
    region_admin = admin.RegionAdmin(Region, AdminSite())

    with monkeypatch.context() as m:
        mock_load_region = mock.Mock()
        m.setattr('unicef_security.admin.load_region', mock_load_region)

        # mock_request = mock.Mock()
        # m.setattr('unicef_security.admin.ExtraUrlMixin', mock.Mock())
        # m.setattr('unicef_security.admin.link', mock.Mock())
        # m.setattr('unicef_security.admin.action', mock.Mock())
        # m.setattr('unicef_security.admin.extras', mock.Mock())
        # m.setattr('admin_extra_urls.extras.ExtraUrlMixin', mock.Mock())
        # m.setattr('admin_extra_urls.extras.link', mock.Mock())
        # m.setattr('admin_extra_urls.extras.action', mock.Mock())
        # m.setattr('admin_extra_urls.extras', mock.Mock())

        with pytest.raises(AssertionError):
            mock_load_region.assert_called_with()
        # region_admin.sync(mock_request)
        # region_admin.sync(mock.Mock())
        request = requests_mock.get(admin.admin_reverse(User))
        region_admin.sync(request)
        mock_load_region.assert_called_with()

def test_business_area_admin_sync(monkeypatch):
    pass

def test_business_area_admin_sync_err(monkeypatch):
    pass

class TestUserAdmin2():
    def test_is_linked(self):
        print('test_is_linked')
        pass
    
    def test_impersonate(self):
        pass
    
    def test_sync_user(self):
        pass
    
    def test_sync_user_err(self):
        pass

    def test_link_user_data(self):
        pass
    
    def test_link_user_data_err(self):
        pass
    
    def test_load(self):
        pass

class TestRoleform():
    pass