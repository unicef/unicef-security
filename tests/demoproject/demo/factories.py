import factory

from unicef_security.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
