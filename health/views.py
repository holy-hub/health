from django.shortcuts import render

# Create your views here.
def main_home(request):
    context = {
        'title': 'Page d\'accueil',
    }
    return render(request, '.html', context)