from unicef_security.utils import get_setting


def test_get_setting_ok(django_app):
    assert (
        get_setting(
            [
                "TIME_ZONE",
            ],
            "DEFAULT",
        )
        == "UTC"
    )


def test_get_setting_default(django_app):
    assert (
        get_setting(
            [
                "NON_EXISTING_SETTING",
            ],
            "DEFAULT",
        )
        == "DEFAULT"
    )
