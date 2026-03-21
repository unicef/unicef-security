from django.contrib.auth.models import AbstractUser

from unicef_security.models import SecurityMixin, TimeStampedModel


class User(TimeStampedModel, SecurityMixin, AbstractUser):
    class Meta(AbstractUser.Meta):
        app_label = "demo"
