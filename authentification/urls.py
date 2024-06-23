from django.urls    import path
from .views         import *

urlpatterns = [
    path('login/',          login,         name='login'        ),
    path('out/',            out,           name='out'          ),
    path('register/',       register,      name='register'     ),
    path('delete-account/', deleteAccount, name='deleteAccount'),
]