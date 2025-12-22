# Admin

The `unicef-security` app provides a custom user admin.

## UserAdminPlus

A custom user admin that adds extra buttons and filters.

### Buttons

- `sync_user`: Synchronizes a user with Azure Active Directory.
- `link_user_data`: Links a user to an Azure Active Directory account.
- `load`: Loads users from Azure Active Directory.
- `ad`: Shows a user's Azure Active Directory data.

### Filters

- `UNICEFUserFilter`: Filters users by whether they are UNICEF users or external users.
