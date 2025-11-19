"""
URL configuration for mapproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mapapp.urls')),
]

# Always serve media files, even when DEBUG is False (development convenience)
if settings.MEDIA_URL:
    media_pattern = settings.MEDIA_URL.lstrip('/')
    urlpatterns.append(
        re_path(r'^%s(?P<path>.*)$' % media_pattern, static_serve, {'document_root': settings.MEDIA_ROOT})
    )
