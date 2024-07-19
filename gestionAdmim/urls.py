from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_adm, name='dashboard_adm'),
    path('login/', log_in, name='connex'),
    path('sign-up/', sign, name='sign'),
    path('verification/', approve, name='approve'),
]