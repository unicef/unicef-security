# Middleware

The `unicef-security` app provides custom middleware for handling social authentication exceptions.

## UNICEFSocialAuthExceptionMiddleware

Middleware that handles exceptions during social authentication.

### Methods

- `process_exception`: Processes exceptions that occur during social authentication.
- `get_redirect_uri`: Returns the redirect URI for the user.
