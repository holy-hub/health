from django.urls    import path
from .views         import *

urlpatterns = [
    path('log/', auth, name='log'),
    path('out/', out, name='out'),
    path('delete-account/', deleteAccount, name='deleteAccount'),
]