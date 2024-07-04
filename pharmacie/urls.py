from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_ph'),
    path('pharmacie/new/', creaPhar, name='create_ph'),
    path('pharmacie/read/phar<int:pha_name>vwRd/', readPhar, name='readOne_ph'),
    path('pharmacie/read/all/', readAllPhar, name='readAll_ph'),
    path('pharmacie/update/phar<int:pha_name>vwUpD/', updPhar, name='update_ph'),
    path('pharmacie/delete/phar<int:pha_name>vwDlp/', delPhar, name='delete_ph'),
    path('maladie/new/', creaIll, name='create_ill'),
    path('maladie/read/ill<int:mal_name>vwRd/', readIll, name='readOne_ill'),
    path('maladie/read/ill/all/', readAllIll, name='readAll_ill'),
    path('maladie/update/ill<int:mal_name>vwUpD/', updIll, name='update_ill'),
    path('maladie/delete/ill<int:mal_name>vwDlp/', delIll, name='delete_ill'),
    path('medication/new/', creaMedoc, name='create_medoc'),
    path('medication/read/medoc<int:medoc_name>vwRd/', readMedoc, name='readOne_medoc'),
    path('medication/read/all/', readAllMedoc, name='readAll_medoc'),
    path('medication/update/medoc<int:medoc_name>vwUpD/', updMedoc, name='update_medoc'),
    path('medication/delete/medoc<int:medoc_name>vwDlp/', delMedoc, name='delete_medoc'),
]