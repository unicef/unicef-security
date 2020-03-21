from social_core.tests.backends.test_azuread_b2c import AzureADOAuth2Test

# class UNICEFAzureADOAuth2Test(AzureADOAuth2Test):
#     backend_path = 'unicef_security.backends.UNICEFAzureADB2COAuth2'


class UNICEFAzureADTenantOAuth2ExtTest(AzureADOAuth2Test):
    backend_path = 'unicef_security.backends.UNICEFAzureADTenantOAuth2Ext'
