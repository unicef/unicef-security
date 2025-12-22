# Graph API

The `unicef-security` app provides a client for interacting with the Microsoft Graph API.

## Synchronizer

A class for synchronizing users with Azure Active Directory.

### Methods

- `get_token`: Gets an access token from Azure Active Directory.
- `get_page`: Gets a page of users from Azure Active Directory.
- `get_record`: Gets a user record from Azure Active Directory.
- `fetch_users`: Fetches users from Azure Active Directory.
- `search_users`: Searches for users in Azure Active Directory.
- `filter_users_by_email`: Filters users by email in Azure Active Directory.
- `get_user`: Gets a user from Azure Active Directory.
- `sync_user`: Synchronizes a user with Azure Active Directory.
- `resume`: Resumes a synchronization with Azure Active Directory.
- `is_valid`: Checks if a user is valid.
- `synchronize`: Synchronizes users with Azure Active Directory.
