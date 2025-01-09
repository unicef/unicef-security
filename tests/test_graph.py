from social_django.utils import load_strategy, load_backend

from demo.models import User
from .factories import GroupFactory, UserFactory
from unicef_security.graph import Synchronizer, get_unicef_user, default_group, SyncResult
import responses
import pytest
from constance import config as constance


@pytest.fixture
def strategy():
    return load_strategy()


@pytest.fixture
def backend(strategy):
    return load_backend(strategy=strategy, name="azuread-b2c-oauth2", redirect_uri="/")


def get_response(email):
    return {
        "id_token": "token",
        "token_type": "Bearer",
        "not_before": 1607541825,
        "id_token_expires_in": 3600,
        "profile_info": "profile_info",
        "scope": "openid",
        "access_token": "access_token",
        "exp": 1607545425,
        "nbf": 1607541825,
        "ver": "1.0",
        "iss": "https://tenant.b2clogin.com/1234567890/v2.0/",
        "sub": "abcdefgh",
        "aud": "abcdefgh",
        "acr": "b2c_1a_unicef_social_signup_signin",
        "iat": 1607541825,
        "auth_time": 1607541824,
        "given_name": "Given",
        "family_name": "Family",
        "name": "Given Family",
        "idp": "UNICEF Azure AD",
        "email": email,
    }


def get_details(email):
    return {
        "username": "Given Family",
        "email": email,
        "unique_name": email,
        "fullname": "Given Family",
        "first_name": "Given",
        "last_name": "Family",
        "idp": "UNICEF Azure AD",
    }


@responses.activate
def test_get_user(django_app):
    responses._add_from_file(file_path="tests/vcr_cassettes/get_user.yaml")
    synchronizer = Synchronizer()
    synchronizer.get_user("ddinicola@unicef.org")


@pytest.mark.django_db
@responses.activate
def test_sync_user(django_app):
    responses._add_from_file(file_path="tests/vcr_cassettes/sync_user.yaml")
    user = UserFactory(username="ddinicola@unicef.org", azure_id="12345678-aaaa-bbbb-cccc-123456789012")
    synchronizer = Synchronizer()
    synchronizer.sync_user(user)
    user.refresh_from_db()
    assert user.first_name == "Domenico"


@pytest.mark.django_db
@responses.activate
def test_fetch_users():
    responses._add_from_file(file_path="tests/vcr_cassettes/fetch_users.yaml")
    synchronizer = Synchronizer()
    synchronizer.fetch_users("startswith(mail,'ddinicola')")
    assert User.objects.get(username="ddinicola@unicef.org")


@pytest.mark.django_db
@responses.activate
def test_search_users():
    responses._add_from_file(file_path="tests/vcr_cassettes/search_users.yaml")
    user = UserFactory(email="ddinicola@unicef.org", first_name="Domenik", last_name="Di Nicola")
    synchronizer = Synchronizer()
    resp = synchronizer.search_users(user)
    assert len(resp) == 1
    assert resp[0]["displayName"] == "Domenico Di Nicola"


@responses.activate
def test_filter_users_by_email():
    responses._add_from_file(file_path="tests/vcr_cassettes/filter_users_by_email.yaml")
    synchronizer = Synchronizer()
    resp = synchronizer.filter_users_by_email("ddinicola@unicef.org")
    assert len(resp) == 1
    assert resp[0]["displayName"] == "Domenico Di Nicola"


@pytest.mark.django_db
@responses.activate
def test_sync_synchronize(django_app):
    responses._add_from_file(file_path="tests/vcr_cassettes/synchronizer.yaml")  # cassette changed manually
    assert User.objects.count() == 0
    synchronizer = Synchronizer()
    synchronizer.synchronize(max_records=20)
    assert User.objects.count() == 4


@pytest.mark.django_db
@responses.activate
def test_resume():
    responses._add_from_file(file_path="tests/vcr_cassettes/synchronizer.yaml")  # cassette changed manually
    assert User.objects.count() == 0
    synchronizer = Synchronizer()
    synchronizer.resume(
        max_records=20,
        delta_link="https://graph.microsoft.com/v1.0/users/delta_changed_manually",
    )
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_default_group_admin():
    email = "ddinicola@unicef.org"
    user = UserFactory(email=email, username=email)
    GroupFactory(name=constance.DEFAULT_GROUP)

    assert not user.is_staff
    assert not user.is_superuser
    assert not user.groups.exists()
    default_group(user=user, is_new=True)
    user.refresh_from_db()
    assert user.is_staff
    assert user.is_superuser
    assert user.groups.count() == 0


@pytest.mark.django_db
def test_default_group():
    email = "simple@unicef.org"
    user = UserFactory(email=email, username=email)
    GroupFactory(name=constance.DEFAULT_GROUP)

    assert not user.groups.exists()
    default_group(user=user, is_new=True)
    user.refresh_from_db()
    assert user.groups.count() == 1


@pytest.mark.django_db
@responses.activate
def test_get_unicef_user(backend):
    responses._add_from_file(file_path="tests/vcr_cassettes/get_unicef_user.yaml")
    email = "ddinicola@unicef.org"
    details = get_details(email)
    response = get_response(email)
    result = get_unicef_user(backend, details, response)
    assert result["is_new"]
    assert result["user"]
    assert result["social"]


@pytest.mark.django_db
def test_get_unicef_user_existing(backend):
    email = "ddinicola@unicef.org"
    user = UserFactory(email=email, username=email)
    user.social_auth.create()
    details = get_details(email)
    response = get_response(email)
    result = get_unicef_user(backend, details, response)
    assert result["user"] == user
    assert result["social"] == user.social_auth.get()
    assert not result["is_new"]


@pytest.mark.django_db
def test_sync_result_log(auth_user):
    result = SyncResult()
    result.log(auth_user, True)
    result.log(auth_user, False)
    result.log(None)
    assert len(result.created) == 1
    assert len(result.updated) == 1
    assert len(result.skipped) == 1


@pytest.mark.django_db
def test_sync_result_add(auth_user):
    result = SyncResult()
    result.log(auth_user, True)
    assert len(result.created) == 1
    assert len(result.updated) == 0

    result2 = SyncResult()
    result2.log(auth_user, False)
    assert len(result2.created) == 0
    assert len(result2.updated) == 1

    result3 = result + result2
    assert len(result3.created) == 1
    assert len(result3.updated) == 1


@pytest.mark.django_db
def test_sync_result_eq(auth_user):
    result = SyncResult()
    result.log(auth_user, True)

    result2 = SyncResult()
    result2.log(auth_user, True)

    assert result == result2

    result3 = SyncResult()
    result3.log(auth_user, False)

    assert result != result3
