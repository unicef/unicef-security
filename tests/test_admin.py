from django.urls import reverse

from mock import patch

import pytest

from unicef_security.admin import UNICEFUserFilter

from demo.admin import UserPlus
from demo.models import User

from .factories import UserFactory


@pytest.mark.django_db
@patch("unicef_security.admin.Synchronizer.get_token")
@patch("unicef_security.admin.Synchronizer.get_user")
@patch("unicef_security.admin.Synchronizer.sync_user")
@patch("unicef_security.admin.Synchronizer.search_users")
def test_link_user_data(patch1, patch2, patch3, patch4, app):
    user = UserFactory()
    url = reverse("admin:demo_user_link_user_data", args=[user.pk])
    res = app.post(url)
    assert res.status_code == 200


@pytest.mark.django_db
@patch("unicef_security.admin.Synchronizer.get_token")
@patch("unicef_security.admin.Synchronizer.fetch_users")
def test_link_load(patch1, patch2, app):
    url = reverse("admin:demo_user_load")
    res = app.post(url)
    assert res.status_code == 200


@pytest.mark.django_db
def test_unicef_admin_filter():
    UserFactory(email="test@unicef.org", username="test@unicef.org")
    UserFactory(email="test@external.com", username="test@external.com")
    qs = User.objects.all()
    assert qs.count() == 2

    filters = UNICEFUserFilter(
        None,
        {
            "email": [
                "unicef",
            ]
        },
        User,
        UserPlus,
    )
    unicef_records = filters.queryset(None, qs)
    assert unicef_records.count() == 1

    filters = UNICEFUserFilter(
        None,
        {
            "email": [
                "external",
            ]
        },
        User,
        UserPlus,
    )
    external_records = filters.queryset(None, qs)
    assert external_records.count() == 1
