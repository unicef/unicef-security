# Models

The `unicef-security` app provides a custom user model and other security-related models.

## SecurityMixin

A mixin model that adds security-related fields to the user model.

### Fields

- `azure_id` (UUIDField): The user's Azure Active Directory ID.
- `job_title` (CharField): The user's job title.
- `display_name` (CharField): The user's display name.

### Properties

- `label`: A cached property that returns the user's display name, full name, or username.

## TimeStampedModel

A model that adds a `last_modify_date` field.

### Fields

- `last_modify_date` (DateTimeField): The date and time the model was last modified.
