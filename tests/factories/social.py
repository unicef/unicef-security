from uuid import uuid4

from social_django.models import UserSocialAuth

import factory

from .user import UserFactory


class SocialAuthUserFactory(UserFactory):
    @factory.post_generation
    def sso(self, create, extracted, **kwargs):
        UserSocialAuth.objects.get_or_create(user=self, provider="test", uid=uuid4())
