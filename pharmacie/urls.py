from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_ph'),
    path('pharmacie/new/', creaPhar, name='create_ph'),
    path('pharmacie/read/phar<int:id>vwRd/', readPhar, name='readOne_ph'),
    path('pharmacie/read/all/', readAllPhar, name='readAll_ph'),
    path('pharmacie/update/phar-mien-vwUpD/', updPhar, name='update_ph'),
    path('pharmacie/delete/phar<int:id>vwDlp/', delPhar, name='delete_ph'),
    path('maladie/new/', creaIll, name='create_ill'),
    path('maladie/read/ill<int:id>vwRd/', readIll, name='readOne_ill'),
    path('maladie/read/ill/all/', readAllIll, name='readAll_ill'),
    path('maladie/update/ill<int:id>vwUpD/', updIll, name='update_ill'),
    path('maladie/delete/ill<int:id>vwDlp/', delIll, name='delete_ill'),
    path('medication/new/', creaMedoc, name='create_medoc'),
    path('medication/read/medoc<int:id>vwRd/', readMedoc, name='readOne_medoc'),
    path('medication/read/all/', readAllMedoc, name='readAll_medoc'),
    path('medication/update/medoc<int:id>vwUpD/', updMedoc, name='update_medoc'),
    path('medication/delete/medoc<int:id>vwDlp/', delMedoc, name='delete_medoc'),
]