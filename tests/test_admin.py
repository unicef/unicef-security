import uuid

import mock
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

import pytest

from unicef_security import admin
from unicef_security.models import BusinessArea, Region, User


def test_admin_reverse():
    model = User
    page = "changelist"
    reversed = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}")
    assert reversed == admin.admin_reverse(User)


def test_region_admin_sync(monkeypatch, requests_mock):
    region_admin = admin.RegionAdmin(Region, AdminSite())

    with monkeypatch.context() as m:
        mock_load_region = mock.Mock()
        m.setattr('unicef_security.admin.load_region', mock_load_region)
        setattr(requests_mock, 'GET', {})

        with pytest.raises(AssertionError):
            mock_load_region.assert_called_with()

        region_admin.sync(requests_mock)
        mock_load_region.assert_called_with()


def test_business_area_admin_sync(monkeypatch, requests_mock):
    ba_admin = admin.BusinessAreaAdmin(BusinessArea, AdminSite())

    with monkeypatch.context() as m:
        mock_load_ba = mock.Mock()
        m.setattr('unicef_security.admin.load_business_area', mock_load_ba)
        setattr(requests_mock, 'GET', {})

        with pytest.raises(AssertionError):
            mock_load_ba.assert_called_with()

        ba_admin.sync(requests_mock)
        mock_load_ba.assert_called_with()


def test_business_area_admin_sync_err(monkeypatch, requests_mock):
    ba_admin = admin.BusinessAreaAdmin(BusinessArea, AdminSite())

    with monkeypatch.context() as m:
        mock_load_ba_err = mock.Mock(side_effect=Exception)
        m.setattr('unicef_security.admin.load_business_area', mock_load_ba_err)
        setattr(requests_mock, 'GET', {})

        with pytest.raises(AssertionError):
            mock_load_ba_err.assert_called_with()

        with pytest.raises(Exception):
            ba_admin.sync(requests_mock)
            # test logger msg

        mock_load_ba_err.assert_called_with()


class TestUserAdmin2():
    @classmethod
    def setup_class(cls):
        cls.TEST_AZURE_GRAPH_API_BASE_URL = 'https://test.com/123'
        cls.useradmin = admin.UserAdmin2(User, AdminSite)

    def test_is_linked(self):
        azure_mock = mock.Mock(return_value={"is_linked": True})
        assert self.useradmin.is_linked(azure_mock) is True

    @pytest.mark.django_db
    @pytest.mark.skip(reason="'impersonate' does not seem to exist")
    def test_impersonate(self, requests_mock):
        self.user = User()
        test_req = self.useradmin.impersonate(requests_mock, self.user.id)
        assert test_req.status_code == 200
        assert test_req.url == reverse('impersonate-start', args=[self.user.id])

    @pytest.mark.django_db
    def test_sync_user(self, requests_mock, monkeypatch):
        self.user = User(azure_id=uuid.uuid1(), display_name='test_user')
        self.user.save()
        with monkeypatch.context() as m:
            test_azr_return = mock.Mock(return_value={'username': 'uname_test'})
            m.setattr('unicef_security.graph.Synchronizer.get_token', test_azr_return)
            m.setattr('unicef_security.graph.Synchronizer.get_page', mock.Mock())
            self.useradmin.sync_user(requests_mock, self.user.id)

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
