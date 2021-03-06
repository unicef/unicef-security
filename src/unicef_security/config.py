import os

AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')

INSIGHT_URL = os.environ.get('INSIGHT_URL', 'https://unibiapitest.azure-api.net/biapi/v1/')
INSIGHT_SUB_KEY = os.environ.get('INSIGHT_SUB_KEY', 'insight_sub_key')

GRAPH_CLIENT_ID = os.environ.get('GRAPH_CLIENT_ID', AZURE_CLIENT_ID)
GRAPH_CLIENT_SECRET = os.environ.get('GRAPH_CLIENT_SECRET', AZURE_CLIENT_SECRET)

AZURE_SSL = True
AZURE_URL_EXPIRATION_SECS = 10800
AZURE_ACCESS_POLICY_EXPIRY = 10800  # length of time before signature expires in seconds
AZURE_ACCESS_POLICY_PERMISSION = 'r'
AZURE_TOKEN_URL = 'https://login.microsoftonline.com/unicef.org/oauth2/token'
AZURE_GRAPH_API_BASE_URL = 'https://graph.microsoft.com'
AZURE_GRAPH_API_VERSION = 'v1.0'
AZURE_GRAPH_API_PAGE_SIZE = 300

UNICEF_EMAIL = os.environ.get('UNICEF_EMAIL', '@unicef.org')
