from django.conf import settings
from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag()
def ad_backend():
    return reverse('social:begin', args=[getattr(settings, "SOCIAL_AUTH_BACKEND_NAME", "azuread-tenant-oauth2")])
