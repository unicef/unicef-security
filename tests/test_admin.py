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
