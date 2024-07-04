from django.shortcuts import render

# Create your views here.
def main_home(request):
    context = {
        'title': 'Page d\'accueil',
    }
    return render(request, 'index.html', context)

def setting(request):
    context = {
        'title': 'Page d\'accueil',
    }
    return render(request, 'setting.html', context)
