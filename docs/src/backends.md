# Backends

The `unicef-security` app provides custom authentication backends.

## UNICEFAzureADTenantOAuth2Ext

An extension of `social_core.backends.azuread_tenant.AzureADTenantOAuth2` that adds support for UNICEF's Azure Active Directory tenant.

### Methods

- `user_data`: Decodes the ID token and returns the user data.
