import os

from django.conf import settings


def env_or_settings(name, default=None):
    return os.environ.get(name, getattr(settings, name, default))


AZURE_CLIENT_ID = env_or_settings('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = env_or_settings('AZURE_CLIENT_SECRET')

INSIGHT_URL = env_or_settings('INSIGHT_URL', 'https://unibiapitest.azure-api.net/biapi/v1/')
INSIGHT_SUB_KEY = env_or_settings('INSIGHT_SUB_KEY', 'insight_sub_key')

GRAPH_CLIENT_ID = env_or_settings('GRAPH_CLIENT_ID', AZURE_CLIENT_ID)
GRAPH_CLIENT_SECRET = env_or_settings('GRAPH_CLIENT_SECRET', AZURE_CLIENT_SECRET)

AZURE_SSL = env_or_settings('AZURE_SSL', True)
AZURE_URL_EXPIRATION_SECS = int(env_or_settings('AZURE_URL_EXPIRATION_SECS', 10800))
AZURE_ACCESS_POLICY_EXPIRY = int(env_or_settings('AZURE_ACCESS_POLICY_EXPIRY', 10800))
AZURE_ACCESS_POLICY_PERMISSION = env_or_settings('AZURE_ACCESS_POLICY_PERMISSION', 'r')
AZURE_TOKEN_URL = env_or_settings('AZURE_TOKEN_URL', 'https://login.microsoftonline.com/unicef.org/oauth2/token')
AZURE_GRAPH_API_BASE_URL = env_or_settings('AZURE_GRAPH_API_BASE_URL', 'https://graph.microsoft.com')
AZURE_GRAPH_API_VERSION = env_or_settings('AZURE_GRAPH_API_VERSION', 'v1.0')
AZURE_GRAPH_API_PAGE_SIZE = int(env_or_settings('AZURE_GRAPH_API_PAGE_SIZE', 300))

UNICEF_EMAIL = env_or_settings('UNICEF_EMAIL', '@unicef.org')
