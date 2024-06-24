from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
@login_required
def dashboard(request):
    context = {
        'title': 'Pharmacien ' + request.user.user.username,
    }
    return render(request, 'dashboard.html', context)

@login_required
def creaPhar(request):
    if request.method == "POST":
        nom         = request.POST.get('nom', '')
        location    = request.POST.get('location', '')
        description = request.POST.get('description', '')
        
        Pharmacie.objects.create(nom=nom, location=location, description=description, pharmacien=request.user).save()
        return redirect('dashboard')
    context = {
        'title': 'Ajout de Pharmacie',
    }
    return render(request, 'create.html', context)

def readPhar(request, pha_id):
    pharmacie = Pharmacie.objects.get(pha_id)
    context = {
        'title'     : 'informations de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'update.html', context)

@login_required
def updPhar(request, pha_id):
    if request.method == "POST":
        pharmacie = Pharmacie.objects.get(pha_id)
        nom      = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')

        if pharmacie.pharmacien == request.user:
            pharmacie.nom, pharmacie.location, pharmacie.description = nom, location, description
            pharmacie.save()
            return redirect('dashboard')
    context = {
        'title'     : 'Mise a jour de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'update.html', context)

@login_required
def delPhar(request, pha_id):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            Pharmacie.objects.get(pha_id).delete()