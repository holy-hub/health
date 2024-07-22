from django.urls import path
from .views import *

urlpatterns = [
    path('login/', auth, name='log'),
    path('login/connexion', log_in, name='log_in'),
    path('login/registration/', log_on_patient, name='log_on'),
    path('login/registration/health/', log_on_sante, name='log_on_sante'),
    path('login/personnel/SANTE', auth_sante, name='log_hos'),
    path('logout/', out, name='out'),
    path('check/email/<str:username>/status/<str:status>', check_status, name='check_status'),
    path('lock/screen/', veille, name='veille '),
    path('check/activity/', check_user_activity, name='check_user_activity'),
    path('delete-account/', deleteAccount, name='deleteAccount'),
    path('redirection/', redirection, name='redirection'),
]