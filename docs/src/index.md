# Welcome to unicef-security documentation

`unicef-security` is a Django app that provides a custom user model and other security-related features for UNICEF applications.

## Core Features

- **Custom User Model**: A custom user model that extends Django's `AbstractUser` with fields for Azure Active Directory integration.
- **Azure AD Integration**: Integration with Azure Active Directory for authentication and user synchronization.
- **Admin Customizations**: Customizations for the Django admin interface to manage users and their Azure AD data.
- **Social Authentication Pipeline**: A social authentication pipeline for creating and updating users from Azure AD.

## Models

The `unicef-security` app provides two models:

- **SecurityMixin**: A mixin model that adds security-related fields to the user model. These fields are used to store user data from Azure Active Directory, such as the user's Azure AD ID, job title, and display name.
- **TimeStampedModel**: A model that adds a `last_modify_date` field to other models.
