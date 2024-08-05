from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def main_home(request, message=''):
    context = {
        'title': 'Page d\'accueil',
        'message': message,
    }
    return render(request, 'index.html', context)

@login_required
def setting(request):
    context = {
        'title': 'Parametres',
    }
    return render(request, 'setting.html', context)

@login_required
def calendar(request):
    context = {
        'title': 'Calendar',
    }
    return render(request, 'calendar.html', context)

def coming_soon(request):
    context = {
        'title': 'Coming Soon !!!',
    }
    return render(request, 'coming_soon.html', context)

def custom_404(request, exception=None):
    context = {
        'title': 'PAGE NON TROUVEE',
        'base': 'medecin_base.html' if request.user.is_medecin else 'pharmacien_base.html' if request.user.is_pharmacien else 'patient_base.html',
    }
    return render(request, '404.html', context, status=404)

def custom_500(request):
    context = {
        'title': 'ERRUR DE SERVEUR',
        'base': 'medecin_base.html' if request.user.is_medecin else 'pharmacien_base.html' if request.user.is_pharmacien else 'patient_base.html',
    }
    return render(request, '500.html', context, status=500)