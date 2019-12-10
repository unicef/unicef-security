from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'social', include('social_django.urls', namespace='social')),
]
