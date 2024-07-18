from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_p'),
    path('appointement/all/', my_appointement, name='my_appointement'),
    path('medecin/all/', all_medecin, name='all_medecin'),
    path('appointement/ask/<str:med_user>/', ask_appointement, name='ask_appointement'),
    path('prescription/all/', prescription, name='prescription'),
    path('carnet-sante/me/', monCarnet, name='monCarnet'),
    path('factures/', factures, name='factures'),
    path('prescription/prsc-<str:prsc_name>-vw7b/', prescription_name, name='prescription_name'),
]