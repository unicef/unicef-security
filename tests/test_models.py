import pytest

from unicef_security.models import Region, AbstractBusinessArea, User
# from unicef_security.models import Region, AbstractBusinessArea


def test_region():
    reg = Region(name="test_name")
    assert str(reg) == 'test_name'


def test_business_area():
    ab = AbstractBusinessArea(name="test_name")
    assert str(ab) == 'test_name'


@pytest.mark.django_db
# def test_user(user):
def test_user():
    user = User(display_name="display_name")
    assert user.label == user.display_name
    user.save()
    assert user.label == user.display_name
    user.delete()

    user = User(first_name="fname", last_name="lname")
    assert user.label == f"{user.first_name} {user.last_name}:"
    assert user.label != user.display_name
    user.save()
    assert user.label == user.display_name
    user.delete()

    user = User(first_name="fname")
    assert user.label == user.first_name
    assert user.label != user.display_name
    user.save()
    assert user.label == user.display_name
    user.delete()

    user = User(username="uname")
    assert user.label == user.username
    assert user.label != user.display_name
    user.save()
    assert user.label == user.display_name
    user.delete()
