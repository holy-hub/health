from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_p'),
    path('appointement/all/', my_appointement, name='my_appointement'),
    path('medecin/all/', all_medecin, name='all_medecin'),
    path('appointement/ask/', ask_appointement, name='ask_appointement'),
    path('prescription/all/', prescription, name='prescription'),
    path('prescription/prsc-<str:prsc_name>-vw7b/', prescription_name, name='prescription_name'),
]