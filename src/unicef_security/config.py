import os


VISION_USER = os.environ.get('VISION_USER', '')
VISION_PASSWORD = os.environ.get('VISION_PASSWORD', '')
AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')

INSIGHT_URL = 'https://devapis.unicef.org/BIService/BIWebService.svc/'

GRAPH_CLIENT_ID = os.environ.get('GRAPH_CLIENT_ID', AZURE_CLIENT_ID)
GRAPH_CLIENT_SECRET = os.environ.get('GRAPH_CLIENT_SECRET', AZURE_CLIENT_SECRET)

AZURE_SSL = True
AZURE_URL_EXPIRATION_SECS = 10800
AZURE_ACCESS_POLICY_EXPIRY = 10800  # length of time before signature expires in seconds
AZURE_ACCESS_POLICY_PERMISSION = 'r'
# AZURE_TOKEN_URL = 'https://login.microsoftonline.com/unicef.org/oauth2/token'
# AZURE_TOKEN_URL = 'https://login.microsoftonline.com/c72354f2-f54d-4829-9fd3-6d5c1b1f71ea/oauth2/token'
# AZURE_TOKEN_URL = 'https://login.microsoftonline.com/csabadenes.onmicrosoft.com/oauth2/token'
# AZURE_TOKEN_URL = 'https://login.microsoftonline.com/9013862a-021b-409e-98eb-6c35397db74e/oauth2/token'
# AZURE_TOKEN_URL = 'https://login.microsoftonline.com/e02822f9-c473-4c77-9343-1c8e6c062f5e/oauth2/token'
AZURE_TOKEN_URL = 'https://login.microsoftonline.com/943a86e8-cb8c-4098-9f0a-46768ed486dd/oauth2/token'
AZURE_GRAPH_API_BASE_URL = 'https://graph.microsoft.com'
# AZURE_GRAPH_API_BASE_URL = 'https://graph.windows.net'
AZURE_GRAPH_API_VERSION = 'v1.0'
AZURE_GRAPH_API_PAGE_SIZE = 300
