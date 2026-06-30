from social_core.tests.backends.test_azuread import AzureADTenantOAuth2Test


class UNICEFAzureADTenantOAuth2ExtTest(AzureADTenantOAuth2Test):
    backend_path = "unicef_security.backends.UNICEFAzureADTenantOAuth2Ext"
