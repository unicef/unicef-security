import mock
from social_core.exceptions import AuthCanceled

from unicef_security.middleware import UNICEFSocialAuthExceptionMiddleware


def test_middleware(django_app):
    request = mock.MagicMock()
    request.META = {
        "LOCATION": "http://example.com",
        "REQUEST_METHOD": "POST",
        "HTTP_OPERATING_SYSTEM_VERSION": "ICE CREAM",
        "HTTP_PLATFORM": "ANDROID",
        "HTTP_APP_VERSION": "1.0.0",
        "HTTP_USER_AGENT": "AUTOMATED TEST",
    }
    request.path = "/testURL/"
    request.session = {}

    middleware = UNICEFSocialAuthExceptionMiddleware(request)

    get_response = mock.MagicMock()
    response = middleware.process_exception(request, AuthCanceled)
    assert get_response.return_value, response
