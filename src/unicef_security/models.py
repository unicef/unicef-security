from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from django_countries.fields import CountryField

app_label = 'unicef_security'


class TimeStampedModel(models.Model):
    last_modify_date = models.DateTimeField(editable=False, blank=True, auto_now=True)

    class Meta:
        app_label = 'unicef_security'
        abstract = True


class Region(TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        app_label = 'unicef_security'

    def __str__(self):
        return f"{self.name}"


class AbstractBusinessArea(models.Model):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    long_name = models.CharField(_('long name'), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = CountryField()

    class Meta:
        app_label = 'unicef_security'
        abstract = True
        verbose_name = _('Business Area')
        verbose_name_plural = _('Business Areas')

    def __str__(self):
        return f"{self.name}"


class BusinessArea(AbstractBusinessArea, TimeStampedModel):
    class Meta:
        app_label = 'unicef_security'
        swappable = 'BUSINESSAREA_MODEL'


class ExtendedAbstractUser(AbstractUser, TimeStampedModel):
    # business_area = models.ForeignKey(settings.BUSINESSAREA_MODEL,
    #                                   null=True, blank=True,
    #                                   on_delete=models.CASCADE)
    azure_id = models.UUIDField(blank=True, unique=True, null=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        abstract = True
        app_label = 'unicef_security'

    @cached_property
    def label(self):
        if self.display_name:
            return self.display_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}:"
        elif self.first_name:
            return self.first_name
        return self.username

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.label
        super().save(*args, **kwargs)


class User(ExtendedAbstractUser):
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        app_label = 'unicef_security'
