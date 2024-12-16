from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import signals

import factory.fuzzy

from .base import AutoRegisterModelFactory


@factory.django.mute_signals(signals.post_save)
class UserFactory(AutoRegisterModelFactory):
    _password = "password"
    username = factory.Sequence(lambda n: "m%03d@unicef.org" % n)
    password = factory.django.Password(_password)
    email = factory.Sequence(lambda n: "m%03d@unicef.org" % n)
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    is_superuser = False
    is_active = True

    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        ret = super()._create(model_class, *args, **kwargs)
        ret._password = cls._password
        return ret


class AdminFactory(UserFactory):
    is_superuser = True


class AnonUserFactory(UserFactory):
    username = "anonymous"


class SuperUserFactory(UserFactory):
    username = factory.Sequence(lambda n: "superuser%03d@example.com" % n)
    email = factory.Sequence(lambda n: "superuser%03d@example.com" % n)
    is_superuser = True
    is_staff = True
    is_active = True


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return  # Simple build, do nothing.

        if extracted:
            for permission in extracted:  # A list of groups were passed in, use them
                self.permissions.add(permission)

    class Meta:
        model = Group
        django_get_or_create = ("name",)