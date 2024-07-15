from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def main_home(request):
    context = {
        'title': 'Page d\'accueil',
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