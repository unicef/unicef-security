import os

import pytest
from django.urls import reverse

from unicef_security import admin
from unicef_security.models import User


def test_admin_reverse():
    model = User
    page="changelist"
    reversed = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}")
    assert reversed == admin.admin_reverse(User)

def test_region_admin_sync():
    pass

def test_business_area_admin_sync():
    pass

def test_business_area_admin_sync_err():
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