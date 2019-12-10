from social_core.tests.backends.test_azuread_b2c import AzureADOAuth2Test


class UnicefAzureADOAuth2Test(AzureADOAuth2Test):
    backend_path = 'unicef_security.backends.UnicefAzureADB2COAuth2'


class AzureADTenantOAuth2ExtTest(AzureADOAuth2Test):
    backend_path = 'unicef_security.backends.AzureADTenantOAuth2Ext'
