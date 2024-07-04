from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
# PHARMACIE
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

def readPhar(request, pha_name):
    pharmacie = Pharmacie.objects.get(nom=pha_name)
    context = {
        'title'     : 'informations de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'read.html', context)

def readAllPhar(request):
    pharmacies = Pharmacie.objects.all()
    context = {
        'title'      : 'informations de Pharmacie',
        'pharmacies' : pharmacies,
    }
    return render(request, 'readAll.html', context)

@login_required
def updPhar(request, pha_name):
    if request.method == "PUT":
        pharmacie = Pharmacie.objects.get(nom=pha_name)
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
def delPhar(request, pha_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            Pharmacie.objects.get(nom=pha_name).delete()

# MALADIE
@login_required
def creaIll(request):
    if request.method == "POST":
        nom           = request.POST.get('nom', '')
        description   = request.POST.get('description', '')
        disease_types = request.POST.get('disease_types', '')
        medication    = request.POST.get('medication', '')
        
        Maladie.objects.create(nom=nom, disease_types=disease_types, description=description, medication=medication).save()
        return redirect('dashboard')
    context = {
        'title': 'Ajout de Maladie',
    }
    return render(request, 'creaMal.html', context)

def readIll(request, mal_name):
    maladie = Maladie.objects.get(nom=mal_name)
    context = {
        'title' : 'informations de la Maladie',
        'maladie' : maladie,
    }
    return render(request, 'readMal.html', context)

def readAllIll(request):
    maladies = Maladie.objects.all()
    context = {
        'title'    : 'informations des Maladies',
        'maladies' : maladies,
    }
    return render(request, 'readAllMal.html', context)

@login_required
def updIll(request, mal_name):
    if request.method == "PUT":
        maladie = Maladie.objects.get(nom=mal_name)
        nom           = request.POST.get('nom', '')
        description   = request.POST.get('description', '')
        disease_types = request.POST.get('disease_types', '')
        medication    = request.POST.get('medication', '')

        if maladie:
            maladie.nom, maladie.description, maladie.disease_types, maladie.medication = nom, description, disease_types, medication
            maladie.save()
            return redirect('dashboard')
    context = {
        'title'   : 'Mise a jour de la Maladie',
        'maladie' : maladie,
    }
    return render(request, 'updateIll.html', context)

@login_required
def delIll(request, mal_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            Maladie.objects.get(nom=mal_name).delete()

# MEDICATION
@login_required
def creaMedoc(request):
    if request.method == "POST":
        nom  = request.POST.get('nom', '')
        role = request.POST.get('role', '')
        prix = request.POST.get('prix', '')
        
        Pharmacie.objects.create(nom=nom, role=role, prix=prix).save()
        return redirect('dashboard')
    context = {
        'title': 'Ajout de Medicament',
    }
    return render(request, 'creaMedoc.html', context)

def readMedoc(request, medoc_name):
    medicament = Medication.objects.get(nom=medoc_name)
    context = {
        'title'      : 'informations de Medication',
        'medicament' : medicament,
    }
    return render(request, 'readMedoc.html', context)

def readAllMedoc(request):
    medication = Medication.objects.all()
    context = {
        'title' : 'informations de Medication',
        'medication' : medication,
    }
    return render(request, 'readAllMedoc.html', context)

@login_required
def updMedoc(request, medoc_name):
    if request.method == "PUT":
        medication = Medication.objects.get(nom=medoc_name)
        nom  = request.POST.get('nom', '')
        role = request.POST.get('role', '')
        prix = request.POST.get('prix', '')

        if medication.pharmacien == request.user:
            medication.nom, medication.role, medication.prix = nom, role, prix
            medication.save()
            return redirect('dashboard')
    context = {
        'title'      : 'Mise a jour de Medication',
        'medication' : medication,
    }
    return render(request, 'updateMedoc.html', context)

@login_required
def delMedoc(request, medoc_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            Medication.objects.get(nom=medoc_name).delete()
