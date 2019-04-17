from unicef_security.models import User

import factory

class UserFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = User
