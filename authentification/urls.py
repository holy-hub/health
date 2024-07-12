from django.urls import path
from .views import *

urlpatterns = [
    path('login/', auth, name='log'),
    path('login/connexion', log_in, name='log_in'),
    path('login/registration/', log_on, name='log_on'),
    path('logout/', out, name='out'),
    path('delete-account/', deleteAccount, name='deleteAccount'),
]