"""
URL configuration for health project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .views import *

# Définition des gestionnaires d'erreur
handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('health/healthy/', admin.site.urls),
    path('', main_home, name='home'),
    path('health/setting/', setting, name='setting'),
    path('health/calendar/', calendar, name='calendar'),
    path('health/coming-soon/', coming_soon, name='coming_soon'),
    path('health/page/not-found/', custom_404),
    path('health/page/error-server/', custom_500),
    path('accounts/', include('authentification.urls')),
    path('medecin/', include('medecin.urls')),
    path('patient/', include('patient.urls')),
    path('pharmacie/', include('pharmacie.urls')),
    path('admin/', include('gestionAdmim.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)