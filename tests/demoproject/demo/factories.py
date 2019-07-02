from django.contrib.auth.models import Group

import factory

from unicef_security.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User


class GroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Group
