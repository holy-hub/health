from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_p'),
    path('appointement/all/', my_appointement, name='my_appointement'),
    path('appointement/motif/', motif, name='motif'),
    path('medecin/all/', all_medecin, name='all_medecin'),
    path('appointement/ask-<int:id>/', ask_appointement, name='ask_appointement'),
    path('prescription/all/', prescription, name='prescription'),
    path('carnet-sante/me/', monCarnet, name='monCarnet'),
    path('factures/', factures, name='factures'),
    path('prescription/prsc-<int:id>-vw7b/', prescription_name, name='prescription_name'),
]