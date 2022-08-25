import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_swagger_view(title=os.getenv(
    'COMPOSE_PROJECT_NAME').replace('-', ' ').upper())


urlpatterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/img/icon.png')),
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
]
