from django.shortcuts import render

# Create your views here.
def dashboard(request):
    context = {
        'title': 'Pharmacien ' + request.user.username,
    }
    return render(request, '.html', context)